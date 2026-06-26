---
name: agent-changelog-commit
description: "Auto-commits workspace file changes with sender attribution after each agent turn"
metadata: { "openclaw": { "emoji": "📝", "events": ["message:sent"], "requires": { "bins": ["git"] } } }
---

# Agent Changelog — Commit

After each outbound message, stages tracked workspace files and queues sender attribution in the commit message body.

Tracked files are read from `.agent-changelog.json` in the workspace, written by `setup.sh` on install.

Part of the `agent-changelog` skill. Install via `setup.sh`.
