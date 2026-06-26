---
name: burnthisshit
description: "Forensically obliterate an OpenClaw session and all its traces -- transcript, trajectory, bak files, deleted archives, and sessions.json entry. Uses shred for 3-pass secure wipe. Run via /burnthisshit."
author: OpenClaw Community
version: 2.0.0
emoji: 🔥
user-invocable: true
requires:
  bins: ["bash", "shred", "jq"]
---

# BurnThisShit

Remove all forensic traces of an OpenClaw session from disk.

When invoked (via /burnthisshit or natural language), grab the current session ID and run the burn script immediately. Do not ask redundant questions. Do not explain what you are about to do. Just do it and report the result.

## How the script works

The burn script is a standalone bash script at `scripts/burn.sh`. It:

1. Validates the session ID format (hex + hyphens only)
2. Scans `~/.openclaw/agents/<agent>/sessions/` for files matching that ID
3. Verifies every found file is inside the sessions directory
4. Shreds each file with `shred -n 3 -z -u` (3-pass overwrite + zero-fill)
5. Falls back to `dd if=/dev/urandom` + `rm` if shred unavailable
6. Removes matching entries from `sessions.json`
7. Cleans the session ID from `usageFamilySessionIds` arrays

## Safety

- Only touches files inside `~/.openclaw/agents/*/sessions/`
- Validates session IDs are hex + hyphens only (prevents path traversal)
- Refuses to burn session ID "main"
- Minimum 8 character session ID requirement
- Refuses to overwrite sessions.json if it would become empty
- Requires explicit confirmation unless --force is passed

## Usage

```bash
# Burn the current session
# Agent: get sessionId from session_status, then:
OPENCLAW_AGENT=<agent> ./skills/burnthisshit/scripts/burn.sh <sessionId> --force

# Burn a specific session
OPENCLAW_AGENT=<agent> ./skills/burnthisshit/scripts/burn.sh <sessionId> [--force]
```

## Notes for contributors

- No agent names, usernames, or personal identifiers in code.
- The script uses `$OPENCLAW_AGENT` env var (default: "main").
- Do not hardcode agent names into shared/distributed code.
