# Observability Layer

## Rationale

Agents fail in ways that are fundamentally different from traditional software: the failure may be 10 tool calls deep, reasoning may be plausible-looking but wrong, and cost can explode silently across sessions. You cannot debug an agent by reading its final output. **You need full traces.**

## What to Instrument

| Signal | Why | How |
|--------|-----|-----|
| Every tool call (name, args, result) | Reconstruct agent behavior | Callback handler |
| Token usage per turn | Cost attribution, budget control | API response metadata |
| Latency per node / tool | Find bottlenecks | Timing wrappers |
| LLM reasoning steps | Understand why agent did X | Message capture |
| Session ID propagation | Cross-turn + cross-agent correlation | State field |
| Error + retry counts | Reliability signals | Exception hooks |

## Real-World Example

An agent silently calls a paid search API 200 times across a session. Without per-turn token + tool tracking, you only discover the $40 bill at end of month. With `AgentTelemetry`, you catch it at call #5 and trigger a budget alert.

## Structured Telemetry Callback

```python
import time
import json
import uuid
from typing import Union
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

class AgentTelemetry(BaseCallbackHandler):
    """
    Full execution trace for debugging, cost tracking, and replay.
    Plug into any observability backend (Langfuse, Datadog, CloudWatch, etc.)
    """
    def __init__(self, session_id: str = None, sink=None):
        self.session_id = session_id or str(uuid.uuid4())
        self.sink = sink or (lambda e: print(json.dumps(e)))
        self.span_stack = []

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.span_stack.append({
            "type": "llm_call", "start": time.monotonic(),
            "session_id": self.session_id,
            "prompt_preview": prompts[0][:200] if prompts else ""
        })

    def on_llm_end(self, response: LLMResult, **kwargs):
        span = self.span_stack.pop() if self.span_stack else {}
        usage = response.llm_output.get("usage", {}) if response.llm_output else {}
        self.sink({
            **span,
            "latency_ms":    int((time.monotonic() - span.get("start", 0)) * 1000),
            "input_tokens":  usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "cache_tokens":  usage.get("cache_read_input_tokens", 0),
            "cost_usd":      self._estimate_cost(usage),
        })

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.span_stack.append({
            "type": "tool_call",
            "tool_name": serialized.get("name", "unknown"),
            "input": input_str[:500],
            "start": time.monotonic(),
            "session_id": self.session_id,
        })

    def on_tool_end(self, output, **kwargs):
        span = self.span_stack.pop() if self.span_stack else {}
        self.sink({**span, "output": str(output)[:500],
                   "latency_ms": int((time.monotonic() - span.get("start", 0)) * 1000)})

    def on_tool_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs):
        span = self.span_stack.pop() if self.span_stack else {}
        self.sink({**span, "error": str(error), "status": "failed"})

    def _estimate_cost(self, usage: dict) -> float:
        # Adjust rates to match your model's pricing
        input_cost  = usage.get("input_tokens",  0) * 0.000015
        output_cost = usage.get("output_tokens", 0) * 0.000075
        cache_cost  = usage.get("cache_read_input_tokens", 0) * 0.0000015
        return round(input_cost + output_cost + cache_cost, 6)


# Usage — attach to any LangGraph invocation
telemetry = AgentTelemetry(session_id="session-abc-123")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "review this PR"}]},
    config={"callbacks": [telemetry]}
)
```

## Cost Tracking

```python
from collections import defaultdict
from dataclasses import dataclass, field

@dataclass
class SessionCostTracker:
    session_id: str
    cost_by_agent: dict   = field(default_factory=lambda: defaultdict(float))
    tokens_by_turn: list  = field(default_factory=list)
    tool_call_counts: dict = field(default_factory=lambda: defaultdict(int))
    total_cost_usd: float = 0.0

    def record_turn(self, agent_name: str, input_tokens: int,
                    output_tokens: int, tools_called: list):
        cost = (input_tokens * 0.000015) + (output_tokens * 0.000075)
        self.total_cost_usd += cost
        self.cost_by_agent[agent_name] += cost
        self.tokens_by_turn.append({"input": input_tokens, "output": output_tokens})
        for tool in tools_called:
            self.tool_call_counts[tool] += 1

    def budget_exceeded(self, limit_usd: float) -> bool:
        return self.total_cost_usd > limit_usd

    def report(self) -> dict:
        return {
            "session_id": self.session_id,
            "total_cost_usd": round(self.total_cost_usd, 4),
            "cost_by_agent": dict(self.cost_by_agent),
            "top_tools": sorted(self.tool_call_counts.items(),
                                key=lambda x: x[1], reverse=True)[:5],
            "turns": len(self.tokens_by_turn),
        }
```

## Distributed Tracing for Multi-Agent

Propagate `trace_id` to all subagents so their spans appear under the same root in your observability platform.

```python
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage

def spawn_subagent_with_trace(subagent, task: str, parent_config: RunnableConfig) -> dict:
    child_config = RunnableConfig(
        callbacks=parent_config.get("callbacks", []),
        tags=[*parent_config.get("tags", []), "subagent"],
        metadata={
            **parent_config.get("metadata", {}),
            "parent_session_id": parent_config.get("metadata", {}).get("session_id"),
            "subagent_task": task[:100]
        }
    )
    return subagent.invoke({"messages": [HumanMessage(task)]}, config=child_config)
```

## Config Snapshot Pattern

Capture all feature flags and environment state at the **start** of each query — never re-read mid-turn. This prevents A/B test flips or remote config changes from creating inconsistent behavior within a single agent turn.

```python
from dataclasses import dataclass
import os

@dataclass(frozen=True)  # frozen = immutable after creation
class QueryConfig:
    """Snapshot of all runtime gates at query entry time."""
    max_output_tokens: int
    enable_streaming: bool
    enable_autocompact: bool
    enable_unattended_retry: bool
    budget_tokens: int | None
    session_id: str

    @classmethod
    def snapshot(cls, session_id: str) -> "QueryConfig":
        """Call once at query start. Pass the result through all nodes."""
        return cls(
            max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS", "8192")),
            enable_streaming=os.getenv("ENABLE_STREAMING", "true").lower() == "true",
            enable_autocompact=os.getenv("ENABLE_AUTOCOMPACT", "true").lower() == "true",
            enable_unattended_retry=os.getenv("UNATTENDED_RETRY", "false").lower() == "true",
            budget_tokens=int(t) if (t := os.getenv("BUDGET_TOKENS")) else None,
            session_id=session_id,
        )

# Usage: snapshot once, pass everywhere
config = QueryConfig.snapshot(session_id="session-abc")
result = agent.invoke(
    {"messages": [HumanMessage("do the task")], "config": config},
    config={"callbacks": [AgentTelemetry(session_id=config.session_id)]}
)
```

**Why this matters:** A remote config service may return a different value for `max_output_tokens` 10 seconds into a 30-second streaming response. Snapshotting at entry ensures the whole turn uses consistent values.

## Tracking Diminishing Returns

Extend telemetry to detect "zombie turns" — continuations that keep running but produce negligible output.

```python
# Add to AgentTelemetry or SessionCostTracker:

@dataclass
class TurnAnalytics:
    session_id: str
    continuation_count: int = 0
    token_deltas: list = field(default_factory=list)

    def record_continuation(self, output_tokens: int, sink=None):
        self.continuation_count += 1
        self.token_deltas.append(output_tokens)

        if sink:
            sink({
                "type": "continuation_analytics",
                "session_id": self.session_id,
                "continuation_num": self.continuation_count,
                "output_tokens": output_tokens,
                "delta_pct_of_prev": (
                    output_tokens / self.token_deltas[-2]
                    if len(self.token_deltas) >= 2 and self.token_deltas[-2] > 0
                    else None
                ),
                "is_diminishing": (
                    len(self.token_deltas) >= 2
                    and all(d < 500 for d in self.token_deltas[-2:])
                )
            })
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Only logging final output | Instrument every tool call and LLM turn — failures happen mid-session |
| No session ID propagation | Pass `session_id` through all subagents for trace correlation |
| No cost budget alert | Add `budget_exceeded()` check after each turn; terminate if exceeded |
| Logging full tool results | Truncate to 500 chars for storage; full results stay in message history |
| Separate traces per subagent | Propagate parent callbacks to all subagents — single root trace |
| Re-reading feature flags mid-turn | Snapshot all config at query entry — changes mid-turn cause inconsistency |
| No continuation analytics | Track token deltas per continuation to detect diminishing returns early |
