# Conversation Memory Sync

Never forget a conversation again. Auto-generates CONVERSATION_LOG.md and ACTIVITY_DIGEST.md from all agent session transcripts.

Use when: you want persistent conversation memory across agent sessions, or when agents keep forgetting past decisions and promises.

## What it does

Solves the #1 problem with AI agents: **they forget everything between sessions**.

This skill includes two Python scripts that run via cron:

1. **sync_conversation_logs.py** — Extracts the last 300 messages from every agent session and writes them to `CONVERSATION_LOG.md` in each agent's workspace. Full messages with timestamps.

2. **sync_activity_digest.py** — Creates a compact 1-line-per-action summary in `ACTIVITY_DIGEST.md`. Ultra-lightweight (~10-20KB per agent).

## Setup

1. Copy the scripts to your workspace
2. Add a cron job: `*/30 * * * * python3 /path/to/sync_conversation_logs.py && python3 /path/to/sync_activity_digest.py`
3. Add to each agent's SOUL.md or AGENTS.md:
   ```
   At EVERY session start, read CONVERSATION_LOG.md and ACTIVITY_DIGEST.md before doing anything else.
   ```

## What gets captured

- All user ↔ agent messages (Telegram, Discord, etc.)
- Cron job outputs and results
- Decisions, promises, task assignments
- Timestamps for everything

## What gets filtered

- Heartbeat noise (HEARTBEAT_OK)
- Empty messages
- System metadata

## File sizes

- CONVERSATION_LOG.md: ~15-20KB per agent (300 messages)
- ACTIVITY_DIGEST.md: ~5-20KB per agent (150 entries, 1 line each)
- Total for 12 agents: ~110KB — zero performance impact

## Requirements

- Python 3.8+
- OpenClaw with session transcripts (default location: ~/.openclaw/agents/*/sessions/*.jsonl)

## Tags
memory, persistence, conversation, logging, multi-agent, session, context, recall
