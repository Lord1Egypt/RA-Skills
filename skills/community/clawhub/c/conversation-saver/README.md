# Conversation Saver

Automatically extract key facts from conversation history and persist to local memory files.

## Features

- **Silent operation**: No user interaction required, runs in background
- **Smart classification**: Routes facts to WARM_MEMORY, MEMORY, ontology, USER.md automatically
- **Hybrid extraction**: Fast regex + LLM semantic understanding
- **Write verification**: Immediate read-after-write to ensure persistence
- **Configurable**: Adjust keywords, filters, and targets via config.json

## Installation

```bash
# From ClawHub (recommended)
clawhub install conversation-saver

# Or manual clone
cd ~/.openclaw/workspace/skills
git clone <your-repo> conversation-saver
```

## Configuration

Edit `config.json` to customize:

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
  }
}
```

## Usage

### Automatic Mode (Recommended)

Add to `AGENTS.md` or `HEARTBEAT.md`:

```markdown
## Post-conversation Hook
After each session → run conversation-saver extract
```

Or schedule via heartbeat:

```bash
uv run ~/.openclaw/workspace/skills/conversation-saver/scripts/extract.py --days 2 --reprocess
```

### Manual Run

```bash
# Preview what would be extracted
uv run scripts/extract.py --days 2 --dry-run

# Execute extraction
uv run scripts/extract.py --days 2

# Extract from specific session
uv run scripts/extract.py --session <sessionKey>
```

## Extraction Example

**Input conversation:**
```
User: My wife goes to Shanghai on business this Wednesday, returns next Tuesday
User: Remember, don't send all photos at once
User: I'm based in Wuhan
```

**Persisted outputs:**

**WARM_MEMORY.md** (Preferences/Schedule):
```markdown
- [2026-03-26] My wife goes to Shanghai on business this Wednesday, returns next Tuesday
- [2026-03-26] Remember, don't send all photos at once
- [2026-03-26] I'm based in Wuhan
```

**ontology** (Person profile):
```json
{
  "id": "xiaomeimei",
  "properties": {
    "notes": "... Mar 26: revealed business trip to Shanghai (Wed-Tue)"
  }
}
```

## How It Works

1. **Collect messages** from memory logs or session history
2. **Rule-based extraction** using regex patterns (fast)
3. **LLM fallback** for implicit facts (configurable)
4. **Classification** routes facts to appropriate files
5. **Deduplication** prevents redundant entries
6. **Persistence** with immediate verification

### Storage Routing

| Fact Type | Destination | Example |
|-----------|-------------|---------|
| Person details | `ontology` + `WARM_MEMORY.md` | Family travel, friend info |
| Time commitments | `WARM_MEMORY.md` | Business trip dates |
| Locations | `USER.md` + `WARM_MEMORY.md` | Hometown, travel |
| Preferences | `WARM_MEMORY.md` | Reply style, photo rules |
| System rules | `TOOLS.md` / `AGENTS.md` | Must @user, concise replies |
| General facts | `MEMORY.md` | Decisions, important notes |

## Customization

### Add Regex Patterns

Edit `scripts/extract.py` → `PATTERNS`:

```python
PATTERNS = {
    "new_type": r"your regex here",
}
```

### Adjust Classification

Modify `classify_fact()` function:

```python
if "keyword" in content:
    fact["category"] = "custom_category"
    fact["targets"] = ["target_file"]
```

## File Structure

```
conversation-saver/
├── SKILL.md
├── config.json
├── scripts/
│   ├── extract.py      # Main entry point
│   ├── persister.py    # File writing with verification
│   └── utils.py        # Helpers (dedupe, etc.)
└── README.md
```

## Debugging

```bash
# Check extraction without writing
uv run scripts/extract.py --today --dry-run

# Force reprocess last 3 days
uv run scripts/extract.py --days 3 --reprocess
```

## Limitations

- Single-user focused (uses `config.json` user_id)
- Language: optimized for English/Chinese keywords
- No vector search (file-based storage only)
- LLM extraction is mocked (needs real implementation for production)

## License

MIT

