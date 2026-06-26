# Tool + Safety Layer

## Rationale

Tools are the only way agents affect the world. If your tool layer is solid, your agent is safe regardless of what the LLM decides to do. If it is weak, no prompt engineering will save you. **Safety rules must be code, not prompts.**

## Tool Design Principles

| Principle | What it means | Why |
|-----------|--------------|-----|
| **Single responsibility** | One tool does one thing | Predictable, easier to guard |
| **Idempotent where possible** | Calling twice = same effect as once | Safe to retry on failure |
| **Deterministic schema** | Input/output types fixed and validated | Prevents injection via malformed args |
| **Explicit over implicit** | `delete_file(path)` not `execute(cmd)` | Allows fine-grained permission rules |
| **Least privilege** | Each agent gets only the tools it needs | Limits blast radius |

## Tool Risk Categories

```
LOW RISK   (always-allow):   read_file, list_dir, search, get_status
MEDIUM RISK (auto-approve):  write_file, create_record, send_notification
HIGH RISK  (human-in-loop):  delete_*, drop_table, deploy, apply_migration
ALWAYS DENY:                  rm -rf /, DROP DATABASE, force_push_main
```

## Tool Definition with Schema

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class WriteFileInput(BaseModel):
    path: str = Field(description="Absolute file path to write")
    content: str = Field(description="Content to write to the file")
    create_dirs: bool = Field(default=False, description="Create parent directories if missing")

@tool(args_schema=WriteFileInput)
def write_file(path: str, content: str, create_dirs: bool = False) -> str:
    """Write content to a file. Creates or overwrites the file at the given path."""
    import os
    if create_dirs:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return f"Successfully wrote {len(content)} characters to {path}"
```

## Permission Guard (GuardedToolNode)

```python
import re
from enum import Enum
from langgraph.types import interrupt, Command
from langgraph.prebuilt import ToolNode
from langchain_core.messages import ToolMessage

class PermissionMode(Enum):
    ALWAYS_ALLOW = "allow"
    ALWAYS_DENY  = "deny"
    ASK          = "ask"

class PermissionRule:
    def __init__(self, tool_pattern: str, arg_pattern: str = None,
                 mode: PermissionMode = PermissionMode.ASK, reason: str = ""):
        self.tool_re = re.compile(tool_pattern)
        self.arg_re  = re.compile(arg_pattern) if arg_pattern else None
        self.mode    = mode
        self.reason  = reason

    def matches(self, tool_name: str, args: dict) -> bool:
        if not self.tool_re.match(tool_name):
            return False
        if self.arg_re:
            return bool(self.arg_re.search(str(args)))
        return True


class GuardedToolNode(ToolNode):
    """
    Applies permission rules before every tool execution.
    Rules evaluated in order — first match wins.
    """
    def __init__(self, tools, rules: list[PermissionRule], audit_log=None):
        super().__init__(tools)
        self.rules = rules
        self.audit_log = audit_log if audit_log is not None else []

    def _check_permission(self, tool_name: str, args: dict):
        for rule in self.rules:
            if rule.matches(tool_name, args):
                return rule.mode, rule.reason
        return PermissionMode.ASK, "no matching rule — defaulting to ask"

    def __call__(self, state):
        tool_calls = state["messages"][-1].tool_calls
        for tc in tool_calls:
            mode, reason = self._check_permission(tc["name"], tc["args"])

            # Audit every call regardless of outcome
            self.audit_log.append({
                "tool": tc["name"], "args": tc["args"],
                "decision": mode.value, "reason": reason,
                "timestamp": __import__("datetime").datetime.utcnow().isoformat()
            })

            if mode == PermissionMode.ALWAYS_DENY:
                return {"messages": [ToolMessage(
                    content=f"DENIED: {reason}", tool_call_id=tc["id"]
                )]}

            if mode == PermissionMode.ASK:
                # Pause — surfaces via result["__interrupt__"]
                # Resume: graph.invoke(Command(resume="yes"), config=config)
                human_decision = interrupt({
                    "type": "tool_approval_request",
                    "tool": tc["name"], "args": tc["args"], "reason": reason,
                    "message": f"Agent wants to call `{tc['name']}`. Approve? (yes/no)"
                })
                if str(human_decision).lower() != "yes":
                    return {"messages": [ToolMessage(
                        content="User denied this tool call.", tool_call_id=tc["id"]
                    )]}

        return super().__call__(state)  # all checks passed


# --- Rule configuration (define once, reuse across agents) ---
DEVOPS_RULES = [
    PermissionRule(r"kubectl_.*", r"(get|describe|logs|top|diff)",
                   PermissionMode.ALWAYS_ALLOW, "read-only kubectl"),
    PermissionRule(r"kubectl_.*", r"(delete|drain|cordon|taint)",
                   PermissionMode.ASK, "destructive cluster operation"),
    PermissionRule(r"kubectl_.*", r"namespace.*production",
                   PermissionMode.ALWAYS_DENY, "production namespace is protected"),
    PermissionRule(r"bash", r"rm\s+-rf\s+/",
                   PermissionMode.ALWAYS_DENY, "dangerous filesystem operation"),
]
```

## Resuming After an Interrupt

```python
from langgraph.types import Command

config = {"configurable": {"thread_id": "session-xyz"}}

# First call — graph pauses at the interrupt
result = app.invoke(
    {"messages": [{"role": "user", "content": "delete the staging namespace"}]},
    config=config
)
print(result["__interrupt__"])  # shows tool_approval_request payload

# Human approves
final = app.invoke(Command(resume="yes"), config=config)

# Human denies
final = app.invoke(Command(resume="no"), config=config)
```

## Remote Killswitch

```python
import httpx
from functools import lru_cache

@lru_cache(maxsize=1)
def fetch_policy(ttl_hash=None) -> dict:
    try:
        r = httpx.get("https://config.internal/agent-policy", timeout=2)
        return r.json()
    except Exception:
        return {"bypass_mode_disabled": True}  # fail safe: restrict on error

def get_ttl_hash(seconds=60):
    import time
    return round(time.time() / seconds)

def is_bypass_mode_allowed() -> bool:
    policy = fetch_policy(ttl_hash=get_ttl_hash(60))
    return not policy.get("bypass_mode_disabled", True)
```

## Tool Result Truncation

Long tool results eat context window tokens. Keep head + tail to preserve semantic meaning.

```python
def truncate_tool_result(result: str, max_chars: int = 10_000) -> str:
    if len(result) <= max_chars:
        return result
    half = max_chars // 2
    return (result[:half]
            + f"\n\n... [{len(result) - max_chars} chars truncated] ...\n\n"
            + result[-half:])
```

## Runtime Concurrency Safety Detection

Schema metadata alone cannot determine if a tool is safe to run concurrently — you need to inspect the actual inputs at call time. A `bash` call with `grep` is safe; the same tool with `rm` is not.

```python
from typing import Protocol
from pydantic import BaseModel

class ConcurrencySafeCheck(Protocol):
    def is_concurrency_safe(self, parsed_input: BaseModel) -> bool: ...

def partition_tool_calls(
    tool_calls: list[dict],
    tools_by_name: dict,
    max_concurrent: int = 10
) -> list[list[dict]]:
    """
    Partition tool calls into batches:
    - Multiple consecutive safe tools → run in parallel (up to max_concurrent)
    - Any unsafe tool → run alone (serial)

    Conservative fallback: if input fails to parse, treat as unsafe.
    """
    batches = []
    current_batch = []

    for tc in tool_calls:
        tool = tools_by_name.get(tc["name"])
        is_safe = False

        if tool and hasattr(tool, "is_concurrency_safe"):
            try:
                schema = tool.args_schema
                parsed = schema.model_validate(tc["args"]) if schema else None
                is_safe = bool(tool.is_concurrency_safe(parsed)) if parsed else False
            except Exception:
                is_safe = False  # parse failure → conservative: treat as unsafe

        if is_safe:
            current_batch.append(tc)
            if len(current_batch) >= max_concurrent:
                batches.append(current_batch)
                current_batch = []
        else:
            if current_batch:
                batches.append(current_batch)
                current_batch = []
            batches.append([tc])  # unsafe tool runs alone

    if current_batch:
        batches.append(current_batch)

    return batches


# Example: tool that declares its own concurrency safety
class BashTool:
    args_schema = BashInput

    def is_concurrency_safe(self, input: BashInput) -> bool:
        """Returns True only for known read-only commands."""
        safe_prefixes = ("grep ", "find ", "ls ", "cat ", "head ", "tail ", "wc ")
        cmd = input.command.strip()
        return any(cmd.startswith(p) for p in safe_prefixes)
```

## Abort Controller Hierarchy

Use a two-level abort hierarchy so a failing tool can cancel its siblings without killing the whole agent query.

```python
import asyncio
from contextlib import asynccontextmanager

class AbortController:
    def __init__(self, parent: "AbortController" = None):
        self._event = asyncio.Event()
        self._parent = parent
        if parent:
            # Propagate parent abort to this child
            asyncio.ensure_future(self._watch_parent())

    async def _watch_parent(self):
        await self._parent.wait()
        self._event.set()

    def abort(self):
        self._event.set()

    async def wait(self):
        await self._event.wait()

    @property
    def aborted(self) -> bool:
        return self._event.is_set()


# Usage in tool execution:
async def execute_tools_concurrently(tool_calls, query_abort: AbortController):
    """
    query_abort: cancelled by user (kills everything)
    sibling_abort: child of query_abort — a single bash failure kills only its siblings
    """
    sibling_abort = AbortController(parent=query_abort)

    async def run_one(tc):
        if sibling_abort.aborted:
            return {"error": "cancelled by sibling failure"}
        try:
            result = await execute_tool(tc)
            return result
        except Exception as e:
            sibling_abort.abort()  # abort siblings, not the whole query
            raise

    return await asyncio.gather(*[run_one(tc) for tc in tool_calls], return_exceptions=True)
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Safety rules in the system prompt | Rules must be code — `GuardedToolNode` with `PermissionRule` |
| No audit log | Log every tool call before executing — essential for debugging and compliance |
| Forgetting `Command(resume=...)` | `interrupt()` pauses the graph; caller must resume with `Command` |
| Generic tool names (`execute`, `run`) | Explicit names (`delete_record`, `deploy_service`) enable fine-grained rules |
| No killswitch for dangerous modes | Add remote config fetch with fail-safe: restrict on fetch error |
| Concurrency check only in schema | Inspect actual inputs at call time — schema can't see bash command content |
| One abort for everything | Two-level hierarchy: query-abort (user cancel) + sibling-abort (peer failure) |
