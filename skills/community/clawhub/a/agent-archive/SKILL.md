---
name: agent-archive
description: >
  Persistent conversation export and replay for AI agents system for Claude Code,
  Caveman, OpenClaw, Hermes, MCP agents, and multi-agent workflows.
  Use when user asks to export, save, archive, persist, snapshot,
  serialize, or backup conversations/chat sessions.
allowed-tools:
  - Write
  - Read
  - Bash
  - Glob
---

# Agent Archive

Persistent conversation export and replay for AI agents.

Supports:

- Markdown export
- JSONL export
- RAG-ready chunking
- Tool call persistence
- Session metadata
- TOC generation
- Long conversation optimization
- Replay-friendly structure
- Auto-summary
- Multi-format export

---

# Export Modes

| Mode | Purpose |
|---|---|
| compact | Human readable |
| full | Full forensic session export |
| rag | Vector DB / RAG ingestion |
| replay | Agent replay & observability |
| jsonl | AI training datasets |

---

# Default Save Paths

```text
.claude/agent-archives/
.claude/agent-archives/jsonl/
.claude/agent-archives/replay/
```

---

# Export Metadata

Always include:

```yaml
session_id:
conversation_id:
exported_at:
model:
agent:
cwd:
message_count:
tool_calls:
export_mode:
```

---

# Long Conversation Rules

If conversation > 30 turns:

- generate TOC
- add anchors
- collapse large tool outputs
- summarize repetitive sections

If conversation > 100 turns:

- split into chunks
- generate session summary
- create chunk index

---

# Tool Call Rules

Preserve:

- tool name
- arguments
- tool result
- timing
- errors
- retry count

Example:

```json
{
  "tool": "Write",
  "success": true,
  "latency_ms": 230
}
```

---

# RAG Export Rules

When using rag mode:

- insert chunk markers
- preserve semantic boundaries
- preserve code fences
- keep markdown headings stable

Chunk format:

```markdown
<!-- chunk:start id=12 -->
...
<!-- chunk:end -->
```

---

# Replay Mode

Replay mode should preserve chronological execution:

1. user input
2. assistant reasoning summary
3. tool call
4. tool result
5. assistant response

This mode is designed for:

- debugging
- benchmarking
- observability
- workflow replay
