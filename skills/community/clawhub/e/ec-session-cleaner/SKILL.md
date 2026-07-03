---
name: session-cleaner
description: Convert raw OpenClaw session JSONL transcripts into clean, readable markdown. Strips tool calls, metadata, and system noise. Keeps the conversation.
---

# Session Cleaner

Converts raw OpenClaw/Clawdbot session JSONL files into clean markdown transcripts.

## What it does

- Reads `.jsonl` session files
- Strips tool calls, system metadata, and noise
- Outputs clean human/assistant conversation markdown
- Supports batch processing across agents

## Scripts

- `session-cleaner.mjs` - Main cleaner (Node.js)
- `session-cleaner-spock.sh` - Batch clean Spock sessions
- `session-cleaner-scotty-remote.sh` - Clean Scotty sessions via SSH
