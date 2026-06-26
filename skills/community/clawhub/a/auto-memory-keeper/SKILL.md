---
name: auto-memory-keeper
description: Auto-capture hourly session highlights and update daily memory files. Keeps long-term memory continuous without manual recording. Triggered by cron or manual "remember this".
version: 1.0.0
---

# Auto Memory Keeper

## Overview

Automatically extract session content and update daily memory files to maintain long-term memory continuity.

**Two modes:**
- **Passive mode**: Cron job runs hourly (automatic)
- **Active mode**: Manual trigger by user ("remember this", "log today")

## How It Works

### Triggers

1. **Auto-trigger**: Cron job runs every hour
2. **Manual trigger**: User says "remember this", "log today", "update memory"

### Workflow

**Step 1: Check Environment**
```bash
DATE=$(date +%Y-%m-%d)
MEMORY_FILE=~/.openclaw/workspace/memory/${DATE}.md

if [ ! -f "$MEMORY_FILE" ]; then
  echo "# ${DATE} Log\n\n## Today's Items\n\n- " > "$MEMORY_FILE"
fi
```

**Step 2: Fetch Recent Sessions**
```python
# Use sessions_list to get active sessions in last 60 minutes
# Use sessions_history to get session details
```

**Step 3: Noise Filtering**

Skip these message types:
- Simple greetings ("hi", "hello", "hey")
- Acknowledgments ("thanks", "ok", "sure", "yes")
- Single word responses
- Questions without context
- HEARTBEAT_OK messages
- System messages

**Step 4: Extract Key Info**

From filtered messages, extract:
| Type | Keywords | Format |
|------|----------|--------|
| **Decision** | "decided", "chose", "adopted" | - {time} {decision} |
| **Task** | new feature, new config, new task | - {time} {task description} |
| **Progress** | "completed", "finished", "installed" | - {time} completed {task} |
| **Issue** | error, bug, failed | - {time} issue: {description} |
| **Conclusion** | summary, conclusion, finding | - {time} {conclusion} |

**Step 5: Smart Deduplication**

Check for duplicates before recording:
```python
# Read current file content
# If similar content exists (>80% similarity), skip
# Otherwise append
```

**Step 6: Update Memory File**

Format:
```markdown
## Today's Items

- {time} {item description}
- {time} {item description}
...
```

### Examples

**Input (user message):**
> "installed openclaw-tavily-search, score 3.639"

**Stored:**
```markdown
- 21:47 installed openclaw-tavily-search skill (score 3.639)
```

**Input (user message):**
> "auto-extract session content to memory file every hour"

**Stored:**
```markdown
- 21:50 created auto-memory-keeper skill for hourly auto memory extraction
```

## Configuration

Configurable via `config.json`:

```json
{
  "memory_dir": "~/.openclaw/workspace/memory",
  "interval_hours": 1,
  "active_minutes": 60,
  "categories": ["Decision", "Task", "Progress", "Issue", "Conclusion"],
  "skip_patterns": ["^hi", "^hello", "^thanks", "^ok"],
  "dedup_threshold": 0.8
}
```

## Quality Rules

1. **Concise** - One sentence per item
2. **Timestamp** - Always include time
3. **Dedupe** - Avoid duplicate entries
4. **Categorize** - Classify by type
5. **Skip noise** - Don't record trivial messages

## FAQ

**Q: How to trigger manually?**
A: Say "remember this", "log today", or "update memory"

**Q: Where is cron configured?**
A: Use `cron job add` command, see example in SKILL.md

**Q: Where are memory files stored?**
A: `~/.openclaw/workspace/memory/YYYY-MM-DD.md`

## Testing

Periodically review memory files and adjust skip_patterns for better filtering.

## Related

- Works well with `session-wrap-up` (manual vs auto trigger)
- Complex memories can be manually written to `MEMORY.md` (long-term)
