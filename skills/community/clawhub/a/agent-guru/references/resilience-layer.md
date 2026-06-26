# Resilience Layer

## Rationale

LLMs are non-deterministic. Tools fail. Networks time out. Rate limits hit. An agent that crashes on first error is not production-grade. **Design for failure as the expected case, not the exception.**

## Error-as-Observation

The most powerful pattern: feed errors back to the LLM as tool results. The LLM can reason about the failure and adapt — try a different approach, ask for clarification, or gracefully degrade.

```python
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolNode

class ResilientToolNode(ToolNode):
    """
    Returns tool execution errors as ToolMessages instead of crashing.
    The LLM observes the error and can reason about next steps.
    """
    def __call__(self, state):
        try:
            return super().__call__(state)
        except Exception as e:
            tool_call_id = state["messages"][-1].tool_calls[0]["id"]
            return {"messages": [ToolMessage(
                content=(
                    f"Tool execution failed: {type(e).__name__}: {str(e)}\n"
                    f"You can try a different approach or ask for clarification."
                ),
                tool_call_id=tool_call_id
            )]}
```

## Retry with Exponential Backoff

```python
import asyncio
import random
from typing import TypeVar, Callable, Awaitable

T = TypeVar("T")

async def with_retry(
    fn: Callable[[], Awaitable[T]],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    retryable_exceptions: tuple = (Exception,)
) -> T:
    """Exponential backoff with jitter — safe for rate-limited APIs."""
    for attempt in range(max_attempts):
        try:
            return await fn()
        except retryable_exceptions as e:
            if attempt == max_attempts - 1:
                raise
            delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
            await asyncio.sleep(delay)
```

## Circuit Breaker

Prevents cascading failures when a downstream tool is consistently failing.

```python
from enum import Enum
import time

class CircuitState(Enum):
    CLOSED    = "closed"     # normal operation
    OPEN      = "open"       # failing — reject calls fast
    HALF_OPEN = "half_open"  # testing if service recovered

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = None

    def call(self, fn, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise RuntimeError(
                    f"Circuit OPEN — service unavailable. "
                    f"Retry after {self.recovery_timeout}s."
                )
        try:
            result = fn(*args, **kwargs)
            self.failure_count = 0
            self.state = CircuitState.CLOSED
            return result
        except Exception:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

# Usage
search_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30.0)

from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    """Search the web."""
    return search_breaker.call(_do_web_search, query)
```

## Max Iteration Guard

Prevents infinite loops — the most common production failure mode for agents.

```python
from typing import TypedDict
from langgraph.graph import END
from langchain_core.messages import AIMessage

class AgentState(TypedDict):
    messages: list
    iteration_count: int
    max_iterations: int

def should_continue(state: AgentState) -> str:
    if state["iteration_count"] >= state["max_iterations"]:
        return "force_stop"
    last = state["messages"][-1]
    return "tools" if getattr(last, "tool_calls", None) else "end"

def increment_counter(state: AgentState) -> AgentState:
    return {**state, "iteration_count": state.get("iteration_count", 0) + 1}

def force_stop_node(state: AgentState) -> AgentState:
    return {**state, "messages": state["messages"] + [AIMessage(
        "Maximum iterations reached. Here is what I accomplished so far..."
    )]}

# In graph:
# graph.add_node("counter", increment_counter)
# graph.add_node("force_stop", force_stop_node)
# graph.add_conditional_edges("agent", should_continue, {
#     "tools": "tools", "force_stop": "force_stop", "end": END
# })
```

## Graceful Degradation

```python
@tool
def search_with_fallback(query: str) -> str:
    """Search with automatic fallback chain."""
    try:
        return premium_search_api(query)      # rich results, paid API
    except Exception:
        try:
            return free_search_api(query)     # basic results, free tier
        except Exception:
            return cached_search_results(query)  # stale but available
```

## Diminishing Returns Detection

Stop a turn not just at an absolute token budget, but when the model starts producing diminishing output per continuation — a "zombie turn" generating only a few tokens per iteration.

```python
from dataclasses import dataclass, field

COMPLETION_THRESHOLD  = 0.90   # stop at 90% of budget consumed
DIMINISHING_THRESHOLD = 500    # token delta below this = diminishing
MIN_CONTINUATIONS     = 3      # apply check only after >= 3 continuations

@dataclass
class TurnBudgetTracker:
    total_budget: int
    tokens_used: int = 0
    continuation_count: int = 0
    recent_deltas: list = field(default_factory=list)

    def record_continuation(self, tokens_this_turn: int) -> None:
        self.tokens_used += tokens_this_turn
        self.continuation_count += 1
        self.recent_deltas.append(tokens_this_turn)
        if len(self.recent_deltas) > 3:
            self.recent_deltas.pop(0)

    def should_stop(self) -> tuple[bool, str]:
        # Hard stop: 90% of budget consumed
        if self.tokens_used >= self.total_budget * COMPLETION_THRESHOLD:
            return True, "budget_threshold"

        # Diminishing returns: >= 3 continuations with tiny deltas
        if (self.continuation_count >= MIN_CONTINUATIONS
                and len(self.recent_deltas) >= 2
                and all(d < DIMINISHING_THRESHOLD for d in self.recent_deltas[-2:])):
            return True, "diminishing_returns"

        return False, ""
```

**Why this matters:** Without diminishing returns detection, an agent can continue a turn indefinitely, producing single-digit token responses per iteration until it hits the absolute limit — accruing input token costs with no useful output.

## Max Output Tokens Escalation Order

When the model hits `max_output_tokens`, escalate before reaching for expensive compaction:

```
1. Escalate output limit → retry with 64k output tokens (same messages, just higher limit)
2. Reactive compact      → compact ONLY if a real 413 API error occurs
3. Context collapse      → staged removal of older message groups
4. Multi-turn recovery   → split response across multiple turns as last resort
```

```python
async def handle_output_limit_error(messages, llm, max_output_tokens=8192):
    """Try escalating output tokens before invoking compaction."""
    escalated_limit = 64_000

    if max_output_tokens < escalated_limit:
        # Step 1: Try same messages with higher limit
        try:
            response = await llm.ainvoke(
                messages,
                max_tokens=escalated_limit
            )
            return response, escalated_limit
        except Exception:
            pass  # fall through to compaction

    # Step 2: Reactive compact (only here, not proactively)
    messages = compact_messages(messages, llm)
    return await llm.ainvoke(messages, max_tokens=escalated_limit), escalated_limit
```

## Streaming Fallback + Orphan Message Cleanup

When streaming fails mid-turn, stale partial state must be cleaned up before retrying non-streaming. Skipping this step causes orphan `tool_results` with stale IDs that poison the fallback response.

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class StreamingState:
    partial_messages: list = None
    pending_tool_results: list = None
    executor: object = None

    def tombstone_and_reset(self) -> "StreamingState":
        """
        Mark all partial messages as abandoned, discard pending tool results.
        Call this before falling back to non-streaming retry.
        """
        # Mark partial assistant messages as tombstoned
        # (prevents 'thinking blocks cannot be modified' API error)
        for msg in (self.partial_messages or []):
            msg.metadata = {**(msg.metadata or {}), "tombstoned": True}

        # Discard pending tool results (they have IDs tied to the failed stream)
        # Return a clean slate
        return StreamingState(
            partial_messages=[],
            pending_tool_results=[],
            executor=None
        )

def retry_with_non_streaming(messages: list, llm, streaming_state: StreamingState):
    """Fallback from streaming to non-streaming after a stream error."""
    clean_state = streaming_state.tombstone_and_reset()
    # Now safe to retry: no orphan tool_results, no partial assistant messages
    return llm.invoke(messages)
```

## Unattended Retry with Heartbeats

For long-running agents in automated pipelines that may wait on rate limits (429/529):

```python
import asyncio
import time
from typing import AsyncGenerator

MAX_BACKOFF_SECONDS    = 5 * 60       # 5 minutes max between retries
BACKOFF_RESET_SECONDS  = 6 * 60 * 60  # reset cap after 6 hours
HEARTBEAT_INTERVAL_SEC = 30           # yield keep-alive every 30s

async def retry_with_heartbeat(
    fn,
    is_unattended: bool = False,
) -> AsyncGenerator:
    """
    Retry indefinitely with exponential backoff + keep-alive heartbeats.
    Use only for truly unattended contexts — not interactive sessions.
    """
    if not is_unattended:
        yield await fn()
        return

    delay = 1.0
    session_start = time.monotonic()
    while True:
        try:
            yield await fn()
            return
        except RateLimitError:
            elapsed = time.monotonic() - session_start
            if elapsed > BACKOFF_RESET_SECONDS:
                delay = 1.0  # reset after 6 hours

            wait_until = time.monotonic() + delay
            while time.monotonic() < wait_until:
                await asyncio.sleep(min(HEARTBEAT_INTERVAL_SEC, wait_until - time.monotonic()))
                yield {"type": "heartbeat", "waiting_for_rate_limit": True}

            delay = min(delay * 2, MAX_BACKOFF_SECONDS)
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Raising exceptions from tools | Return errors as `ToolMessage` — LLM observes and adapts |
| No max iteration limit | Always set `max_iterations`; log and summarize on force-stop |
| No diminishing returns check | Track token deltas per continuation — stop when output is shrinking |
| Jumping to compaction on output limit | Escalate `max_output_tokens` first — same messages, just higher limit |
| Skipping streaming cleanup on fallback | Tombstone partial messages before retrying non-streaming |
| Retry without jitter | Add `random.uniform(0, 1)` to avoid thundering herd |
| Circuit breaker threshold too high | 3-5 failures is typical; tune to API's normal error rate |
| No fallback chain for critical tools | Every tool that can fail needs a degraded alternative |
| Heartbeat retry in interactive sessions | Unattended retry must be gated behind a flag — confuses interactive users |
