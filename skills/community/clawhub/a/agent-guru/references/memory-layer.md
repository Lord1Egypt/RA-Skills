# Memory Layer

## Rationale

An agent without persistent memory repeats mistakes across sessions, loses hard-won context, and forces users to re-explain everything. Memory is not one thing — it is three distinct tiers with different access patterns, lifetimes, and costs.

## Three Memory Tiers

```
┌──────────────────────────────────────────────────────────┐
│  SHORT-TERM (message history)                            │
│  Lifetime: current session                               │
│  Storage: in-memory list / graph state                   │
│  Problem: grows unbounded → hits context window limit    │
│  Solution: auto-compaction (summarize + truncate)        │
├──────────────────────────────────────────────────────────┤
│  WORKING MEMORY (structured state)                       │
│  Lifetime: current task / session                        │
│  Storage: graph state dict / Pydantic model              │
│  Purpose: task progress, intermediate results, flags     │
│  Example: {"files_reviewed": 3, "issues_found": [...]}   │
├──────────────────────────────────────────────────────────┤
│  LONG-TERM (external store)                              │
│  Lifetime: permanent / user-scoped                       │
│  Storage: vector DB, relational DB, key-value store      │
│  Purpose: user preferences, past decisions, knowledge    │
│  Access: retrieved via search, not injected in full      │
└──────────────────────────────────────────────────────────┘
```

## Auto-Compaction (Context Window Management)

When message history approaches the context window limit, summarize and compress. Trigger at 80% of the model's context window.

### Tiered Compaction Order

**Critical:** Apply these steps in order before triggering full autocompact. Each earlier step can free enough tokens to avoid the expensive summary step.

```
1. Tool result budgeting   — cap per-message result size (e.g. 10k chars max)
2. Snip                    — drop oldest non-essential messages
3. Microcompact            — inline compression of intermediate results
4. Autocompact (last resort) — full conversation summary at 80% threshold
5. Reactive compact        — ONLY triggered by a real 413 API error (not proactive)
```

If you jump straight to step 4, you spend model tokens on a summary when step 1-3 would have freed enough space.

### Production Thresholds

```python
AUTOCOMPACT_TRIGGER     = 0.80    # trigger at 80% of context window
AUTOCOMPACT_BUFFER_TOKENS = 13_000  # cushion below hard limit
SUMMARY_RESERVE_TOKENS  = 20_000  # reserve for summary output (p99 = 17.3k observed)
MAX_COMPACT_FAILURES    = 3       # stop retrying after 3 consecutive failures
KEEP_RECENT_MESSAGES    = 10      # always keep the most recent N messages intact
```

### Compaction Implementation

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def estimate_tokens(messages: list) -> int:
    """Rough estimate: 4 chars ≈ 1 token."""
    return sum(len(str(m.content)) for m in messages if hasattr(m, "content")) // 4

def should_compact(messages: list, model_context_window: int = 128_000) -> bool:
    return estimate_tokens(messages) > int(model_context_window * 0.80)

def compact_messages(messages: list, llm, keep_recent: int = 10) -> list:
    """
    Summarize old messages, keep system prompt and recent turns.
    Preserves: key decisions, findings, user preferences, task state.
    Discards: repetitive exchanges, verbose tool outputs, dead-ends.
    """
    if not messages:
        return messages

    system_msgs  = [m for m in messages if isinstance(m, SystemMessage)]
    non_system   = [m for m in messages if not isinstance(m, SystemMessage)]

    if len(non_system) <= keep_recent:
        return messages

    to_summarize = non_system[:-keep_recent]
    to_keep      = non_system[-keep_recent:]

    summary_prompt = (
        "Summarize this conversation history concisely.\n"
        "Preserve: key decisions, findings, user preferences, task state.\n"
        "Discard: repetitive exchanges, verbose tool outputs, dead-ends.\n\n"
        + "\n".join(f"{m.__class__.__name__}: {m.content}" for m in to_summarize)
    )

    summary = llm.invoke([HumanMessage(content=summary_prompt)])
    compact_message = AIMessage(
        content=f"[CONVERSATION SUMMARY — prior context]\n{summary.content}"
    )
    return system_msgs + [compact_message] + to_keep


# In LangGraph — add as a preprocessing node before the agent
def context_management_node(state: dict) -> dict:
    messages = state.get("messages", [])
    compact_failures = state.get("compact_failures", 0)

    # Stop retrying after MAX_COMPACT_FAILURES consecutive failures
    if compact_failures >= 3:
        return state

    if should_compact(messages):
        try:
            messages = compact_messages(messages, llm)
            return {**state, "messages": messages, "was_compacted": True, "compact_failures": 0}
        except Exception:
            return {**state, "compact_failures": compact_failures + 1}
    return state
```

## Memory Injection (AGENT.md Pattern)

Persistent context — team conventions, project rules, domain knowledge — should always be available without retrieval. Store in `AGENT.md` files and inject into every system prompt.

```python
import os
from pathlib import Path

def load_memory_files(search_dirs: list[str]) -> str:
    """Discover and load persistent memory files from known locations."""
    memory_content = []
    for directory in search_dirs:
        for filename in ["AGENT.md", "MEMORY.md", ".agent-context.md"]:
            path = Path(directory) / filename
            if path.exists():
                memory_content.append(f"# From {path}\n{path.read_text()}")
    return "\n\n---\n\n".join(memory_content)

def build_system_prompt(base_prompt: str, working_dir: str) -> str:
    memory = load_memory_files([
        working_dir,
        os.path.expanduser("~/.agent"),
        "/etc/agent/global"
    ])
    if memory:
        return f"{base_prompt}\n\n## Project Context (always apply)\n\n{memory}"
    return base_prompt
```

## Long-Term Memory with Vector Store

```python
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
import uuid

class AgentMemoryStore:
    """
    Long-term episodic memory.
    Stores key decisions, findings, and preferences — searchable by similarity.
    """
    def __init__(self, persist_dir: str, embeddings: Embeddings):
        self.store = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )

    def remember(self, content: str, metadata: dict = None):
        doc = Document(
            page_content=content,
            metadata={
                "id": str(uuid.uuid4()),
                "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
                **(metadata or {})
            }
        )
        self.store.add_documents([doc])

    def recall(self, query: str, k: int = 5, filter: dict = None) -> list[str]:
        docs = self.store.similarity_search(query, k=k, filter=filter)
        return [d.page_content for d in docs]

    def inject_relevant_memories(self, query: str, system_prompt: str) -> str:
        memories = self.recall(query)
        if not memories:
            return system_prompt
        memory_block = "\n".join(f"- {m}" for m in memories)
        return f"{system_prompt}\n\n## Relevant past context\n{memory_block}"
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No compaction threshold | Set at 80% of context window; agent crashes or truncates at 100% |
| Skipping tiered compaction | Apply tool result budgeting + snip before triggering full autocompact |
| Summarizing too aggressively | Keep last 10 messages intact — recent context is most relevant |
| No compact failure circuit breaker | After 3 consecutive autocompact failures, stop retrying (agent is likely stuck) |
| Injecting full long-term store | Retrieve top-K relevant memories; never inject everything |
| No PII controls in vector store | Apply encryption/retention policy before storing user data |
| Working state untyped | Use `TypedDict` or Pydantic model — prevents silent state corruption |
