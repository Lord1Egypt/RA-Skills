---
name: session-recall
description: Recover conversation context when a message arrives with unclear meaning. Use when a user's message lacks context (e.g. "I logged in" with no prior mention of logging in), when resuming after compaction or session reset, or when switching between channels and losing thread. Searches session transcripts, channel summaries, memory files, and cross-channel history to reconstruct context before asking the user.
---

# Session Recall

Recover missing conversation context autonomously. *Never ask the user "what are you talking about?" until all steps are exhausted.*

## When This Triggers

- An incoming message doesn't match the current session context
- Session starts after compaction (`.jsonl.reset` exists)
- User references something not in current context window
- User references a topic from another channel or a cron-delivered notification
- Thread reply arrives without visible parent context

## Recovery Flow

Execute steps in order. Stop early if sufficient context is found.

### Step 0: sessions_history (fastest check)
Use `sessions_history` to retrieve recent messages for the current channel. This requires no file I/O and is the quickest way to recover recent context.

### Step 1: Same-channel transcript
Read the `.jsonl` transcript for the current session:
1. Look up the session associated with this channel via `sessions_list` or `sessions.json`
2. Read `~/.openclaw/agents/{agent}/sessions/{sessionId}.jsonl` (default agent: `main`)
3. For large files, read the **tail** first (`tail -n 200`) rather than loading the entire file
4. Check for `.reset` files with the same sessionId prefix (pre-compaction data)
5. If the message is a thread reply, read the parent message first

### Step 2: Channel context summary
Read `memory/channel_context/{channel-name}.md` if it exists. These are user-maintained summaries of ongoing topics per channel — not a built-in OpenClaw feature, but a recommended convention.

### Step 3: Cross-channel and cron search
Messages often originate from cron jobs or other channels.

1. Extract key terms from the unclear message
2. Use the bundled search script or grep across all `.jsonl` files:
   ```bash
   ./scripts/search_sessions.sh "keyword"
   ```
3. Also search for the current channel ID in other sessions — cron jobs send messages to channels but these don't appear in the channel's own `.jsonl`:
   ```bash
   ./scripts/search_sessions.sh "{current_channel_id}"
   ```
4. When a match is found, read surrounding context to understand the full conversation
5. Sort results by timestamp, prioritize most recent

### Step 4: Memory files
1. `memory/active_context.md` — current shared context across channels
2. `memory/YYYY-MM-DD.md` — today and yesterday's daily notes
3. Semantic memory search if available in your setup (e.g., `memory_search` tool)

### Step 5: Ask the user (last resort)
Only after steps 0–4 yield nothing. Be specific about what was searched:
> "Searched this channel's transcript, cross-channel sessions (including cron), and memory files for '{keyword}' but couldn't find context. What are you referring to?"

## Key Insight: Cron-to-Channel Messages

Cron jobs can send messages to channels via `sessions_send` or direct API calls. These messages:
- Appear in the chat platform for the user to see
- Are logged in the *cron session's* `.jsonl`, NOT the target channel's `.jsonl`
- Require Step 3's channel-ID search to discover

This is the most common cause of unrecognized messages — the user is responding to something a cron job sent.

## Security Note

Session transcripts may contain sensitive data (API keys, passwords, personal information). Do not pipe search output to public channels or logs. This skill assumes single-user/single-agent deployment.

## Notes

- Path `~/.openclaw/agents/main/sessions/` assumes default agent name `main`. Adjust if using a custom agent name.
- Channel context files (`memory/channel_context/`) are a recommended convention, not built-in. Users create and maintain these themselves.
- The search script requires `python3`, `grep`, and `bash`.
