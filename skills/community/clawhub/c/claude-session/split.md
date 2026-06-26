# Session Split

Analyze topic boundaries in the current conversation or a specific session and recommend split points.

## Quick Start

```
/session split                     # Recommend split for current conversation
/session split <session_id>        # Recommend split for specific session
/session split --execute           # Recommend and execute immediately
```

## Instructions

### 1. Determine Target Session

- No arguments: Analyze **current conversation** (look up session ID → read JSONL)
- `<session_id>` specified: Read that session's JSONL

Look up current session ID:

Use the `/session id` topic to look up the current session ID.

### 2. Topic Boundary Analysis

Read user messages in chronological order and identify **topic transition points**.

#### Topic Transition Signals

| Signal | Example |
|--------|---------|
| Subject change | "Never mind that, moving on to..." |
| New file/directory work starts | Before: `apps/dt/` → After: `.ralph/PROMPT.md` |
| Slash command switch | `/sync diff` → `/ralph prompt` |
| Time gap | 30+ minute gap between messages |
| Explicit task completion | "commit", "done", "next" |

#### Analysis Method

```bash
# Extract user messages + timestamps
grep '"type":"user"' ~/.claude/projects/{project}/{session}.jsonl \
  | jq -r '[.timestamp, (.message.content[]? | select(.type=="text") | .text[:100])] | @tsv'
```

### 3. Split Recommendation Output

Group by topic and output as a table:

```markdown
## Split Recommendation: {session_title}

| # | Topic | Message Range | Key Content |
|---|-------|--------------|-------------|
| 1 | WBS file management | 1~15 | WBS download path change, file rename |
| 2 | Ralph PROMPT.md improvement | 16~25 | Commit split rules, BLOCKED skip added |
| 3 | sync diff | 26~30 | fetch-issues --state all bug fix |

### Recommendation
- Topics 1, 3 are related to `sync` → can keep as one session
- Topic 2 is independent → recommend splitting

### Split Point
- **Split before message #16** → Separate topic 1(+3) from topic 2
```

### 4. Execute (`--execute`)

> split_session works in the **opposite direction from intuition**:
>
> | Result | Actual Content |
> |--------|---------------|
> | **New session** | Messages **before** split point (front part) |
> | **Original session** | Messages **after** split point (back part) |

```
mcp__claude-sessions-mcp__split_session({
  project_name: "<project>",
  session_id: "<id>",
  split_index: <message_index>
})
```

After splitting, assign topic titles to each session with `rename-session.sh`:
```bash
bash scripts/rename-session.sh <new_session_id> "topic title"
bash scripts/rename-session.sh <original_session_id> "topic title"
```

## Notes for Current Conversation Analysis

Since the current conversation's JSONL is not yet finalized:
- **Always look up and output the Session ID** — invoking the `/session id` topic is mandatory (no exception for the current conversation)
- Identify topic transition points directly from conversation context
- Recommend using **topic summary + boundary description** instead of message indices
- `--execute` is not available for the current conversation (run after session ends)

## Requirements

- claude-sessions-mcp MCP server required
- `scripts/find-session-id.sh` (current session ID lookup)
