---
name: conversation-saver
description: Automatically extract key facts from conversation history and persist to local memory files. Silent background operation with rule+LLM hybrid extraction.
version: 0.1.1
author: Laobu
source: https://clawhub.ai/laobu/conversation-saver
---

# Conversation Saver

Automatically extracts key facts from your conversations and persists them to the appropriate local memory files (WARM_MEMORY.md, MEMORY.md, ontology, USER.md). Works silently in the background without interrupting the user flow.

## When to Use

- You want your agent to **remember important details** from conversations automatically
- You need **hands-off fact extraction** (no interactive questioning)
- You want facts categorized into the right places (preferences, schedules, person details)
- You prefer **local-first persistence** (no external dependencies)

## How It Works

### 1. Extraction Pipeline

```
Raw Messages → Rule-Based Filter → LLM Extraction → Classification → Deduplication → Persistence
```

- **Rule-Based**: Fast keyword/regex matching for obvious facts (dates, locations, names)
- **LLM**: Step 3.5 Flash extracts structured facts from ambiguous conversations
- **Classification**: Routes facts to the correct storage target
- **Deduplication**: Avoids recording the same fact multiple times

### 2. Storage Targets

| Fact Type | Destination | Example |
|-----------|-------------|---------|
| Person details (family, friends) | `ontology` + `WARM_MEMORY.md` (家庭) | "老婆去上海出差" |
| Time commitments | `WARM_MEMORY.md` (日程) | "下周二回来" |
| Locations | `USER.md` + `WARM_MEMORY.md` | "常驻武汉" |
| Preferences | `WARM_MEMORY.md` (互动偏好) | "不要一股脑发照片" |
| System rules | `TOOLS.md` / `AGENTS.md` | "回复必须@老布" |
| Important decisions | `MEMORY.md` | "决定用Tailwind" |

### 3. Trigger Modes

- **On Session End**: Automatically run after each conversation (requires AGENTS.md hook)
- **Heartbeat Backfill**: Scan recent days for missed conversations (configurable)
- **Manual**: `uv run scripts/extract.py --session <sessionKey>` or `--days N`

## Installation

```bash
# From ClawHub (recommended)
clawhub install conversation-saver

# Or manual
cd ~/.openclaw/workspace/skills
git clone <your-repo> conversation-saver
```

## Configuration

Edit `config.json` to customize behavior:

```json
{
  "extraction": {
    "enabled": true,
    "auto_on_session_end": true,
    "heartbeat_reprocess_days": 2,
    "min_confidence": 0.6,
    "max_facts_per_session": 10
  },
  "filters": {
    "user_id": "ou_39f0f10fb55c7c782610cad6a97f4842",
    "ignore_bot_messages": true,
    "ignore_short_messages": true,
    "min_message_length": 5
  },
  "persistence": {
    "verify_after_write": true,
    "backup_before_write": false,
    "deduplicate_across_sessions": true
  }
}
```

## Usage

### Automatic Mode (Recommended)

Add to `AGENTS.md` to run after each session:

```markdown
## Session End Hooks
- 每次会话结束 → 运行 conversation-saver
```

Or integrate into your existing heartbeat:

```bash
uv run ~/.openclaw/workspace/skills/conversation-saver/scripts/extract.py --days 2 --reprocess
```

### Manual Run

```bash
# Extract from specific session
uv run scripts/extract.py --session <sessionKey>

# Backfill last 3 days
uv run scripts/extract.py --days 3 --reprocess

# Dry run (show what would be extracted)
uv run scripts/extract.py --session <sessionKey> --dry-run
```

## Files Structure

```
conversation-saver/
├── SKILL.md
├── config.json
├── scripts/
│   ├── __init__.py
│   ├── extract.py      # Main entry point
│   ├── classifier.py   # Fact classification
│   ├── persister.py    # File writing with verification
│   └── utils.py        # Helpers (dedupe, date parsing)
└── README.md
```

## Customization

### Add Keywords

Edit `scripts/extract.py` → `KEYWORD_CATEGORIES`:

```python
KEYWORD_CATEGORIES = {
    "person": ["老婆", "小美美", "包子", "家人", "朋友"],
    "location": ["武汉", "上海", "郑州", "出差", "旅行"],
    "time": ["周三", "周二", "本周", "下周", "月", "日"],
    "preference": ["喜欢", "不要", "记住", "记得", "规则"]
}
```

### Adjust LLM Prompt

Modify `scripts/extract.py` → `LLM_EXTRACTION_PROMPT` to change extraction style or output format.

## Requirements

- Python 3.10+
- OpenClaw agent with tool access (read, write, edit)
- StepFun model (for LLM extraction)

## Testing

```bash
# Dry run on today's conversations
uv run scripts/extract.py --today --dry-run

# Check extracted facts count
uv run scripts/extract.py --today --stats-only
```

## Limitations

- **Single-user focus**: Designed for one primary user (your USER.md)
- **No vector search**: Facts are stored in files, not semantic searchable (yet)
- **Language**: Optimized for Chinese conversations (keywords in Chinese)
- **No GUI**: All configuration via config.json

## Credits

Inspired by `openclaw-user-profiler`'s structured approach and `elite-longterm-memory`'s tiered architecture.
