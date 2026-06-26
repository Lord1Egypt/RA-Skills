# Agent Installation Guide

This project is designed to be embedded into an agent workspace.

## Primary integration surface

The primary integration surface is the Python `Journal` API.

```python
from agent_memory import Journal

j = Journal(root=".")
j.init()
j.note("Observed a durable preference")
hits = j.recall("preference")
```

Use the CLI only as a convenience layer for shell workflows, cron jobs, and manual operations.

## Default installation

1. Clone the repository into the workspace:

```bash
git clone git@github.com:misolith/agent-memory-journal.git skills/agent-memory
```

2. Ensure the Python package is importable by the agent runtime.

Examples:
- install it into the runtime environment with `pip install .`
- or add the repository root to `PYTHONPATH`

3. Initialize memory in the workspace root.

Python-first:

```python
from agent_memory import Journal
j = Journal(root=".")
j.init()
```

Optional CLI path:

```bash
ln -sf "$PWD/skills/agent-memory/agent_memory_journal.py" "$PWD/bin/agent-memory-journal"
chmod +x "$PWD/skills/agent-memory/agent_memory_journal.py"
agent-memory-journal --root "$PWD" init
```

This creates:

```text
.memory/
├── AGENT.md
├── config.json
├── core/
├── episodic/
├── sessions/
├── index/
└── archive/
```

## Agent bootstrap instructions

For agents, the recommended startup contract is:

1. Read `.memory/AGENT.md`
2. Use `agent-memory-journal search --query "..."` for deep recall
3. Use `agent-memory-journal note "..."` for episodic observations
4. Use `agent-memory-journal remember "..." --category ...` for durable facts
5. Run `agent-memory-journal ingest` during maintenance / heartbeat cycles

## Hot memory target override

By default, pinned hot memory is promoted into:

- `.memory/AGENT.md`

You can override that by editing `.memory/config.json`.

### Default config

```json
{
  "hot_path": "AGENT.md",
  "hot_header": "# AGENT.md",
  "hot_max_chars": 2048
}
```

`hot_max_chars` is enforced as a **character limit**.
It is not token-aware yet. That is a deliberate tradeoff so the project stays dependency-light for now.

### Example: promote hot memory to workspace root `AGENTS.md`

```json
{
  "hot_path": "../AGENTS.md",
  "hot_header": "# AGENTS.md - Auto-generated hot memory",
  "hot_max_chars": 4000
}
```

This makes `ingest` and `rebuild_agent_md()` write the pinned hot set into the workspace root `AGENTS.md` instead of `.memory/AGENT.md`.

## Future enhancement

A later version may support a tokenizer-backed limit like `hot_max_tokens`, but that is not implemented yet.
Until then, document and treat the hot budget as chars, not tokens.

## Recommended pattern

- Keep `.memory/AGENT.md` as the default hot set for most agents.
- Override `hot_path` only when the host framework already has a canonical root memory file, for example:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `SYSTEM.md`

## Safety note

If you override `hot_path` to a root-level file, that file becomes generated output. Do not manually edit it unless your workflow explicitly supports round-tripping generated memory files.
