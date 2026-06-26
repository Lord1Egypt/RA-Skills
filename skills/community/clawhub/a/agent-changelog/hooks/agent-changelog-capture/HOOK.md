---
name: agent-changelog-capture
description: "Captures sender identity before each agent turn for commit attribution"
metadata: { "openclaw": { "emoji": "📸", "events": ["message:received"] } }
---

# Agent Changelog — Capture

Writes sender identity to `.version-context` in the workspace before each agent turn. The companion `agent-changelog-commit` hook reads this to attribute git commits to the correct user.

Part of the `agent-changelog` skill. Install via `setup.sh`.
