# Memory Augment Skill

> Provide long-term memory for OpenClaw agents. Store, retrieve, and query conversation history across sessions.

## Quick Start

```bash
# Install via clawhub
npx clawhub install memory-augment

# Or clone manually
git clone https://clawhub.ai/skills/memory-augment.git ~/.openclaw/skills/memory-augment

# Store a memory
clawhub memory store "User prefers Python for automation scripts"
```

## Features

- ✅ **Persistent storage**: Memories survive across agent restarts
- ✅ **Semantic search**: Find memories using natural language
- ✅ **Automatic context**: Inject relevant memories before each turn
- ✅ **Type-based scoring**: Preferences > decisions > learning > context
- ✅ **Expiry management**: Temporary memories auto-expire
- ✅ **JSON & Markdown** output formats

## Usage

### Store Memories
```bash
# Basic storage
clawhub memory store "My workspace is at /home/marek/.openclaw/workspace"

# With type and tags
clawhub memory store "Approved inbox-triage for publishing" \
  --type decision --tag income --tag skills
```

### Search Memories
```bash
# Natural language search
clawhub memory search "what did I decide about income?"

# Filter by tag
clawhub memory search "skills" --tag skills
```

### List Memories
```bash
# List all decisions
clawhub memory list --type decision

# List since specific date
clawhub memory list --since "2026-04-14"

# List with tag filter
clawhub memory list --tag income
```

### Delete Memories
```bash
# Delete by ID
clawhub memory delete <uuid>

# Delete old temporary memories
clawhub memory delete --older-than "7d"
```

## Configuration

Edit `config.yaml` to customize:

```yaml
# Storage settings
storage:
  path: ~/.memory-augment/storage.yaml

# Expiry and limits
settings:
  max_memories: 1000
  default_expiry: 7  # days

# Search behavior
search:
  top_k: 20
  min_score: 0.3
```

## Memory Types

### preference
User preferences, coding style, tool choices.
```bash
clawhub memory store "Prefers minimal markdown formatting" --type preference
```

### decision
Decisions made, approvals, blocking choices.
```bash
clawhub memory store "Published inbox-triage skill" --type decision
```

### context
Session context, project state, ongoing work.
```bash
clawhub memory store "Building memory-augment skill" --type context
```

### learning
What the agent learned, patterns discovered.
```bash
clawhub memory store "Sub-agent spawning reduces context by 30%" --type learning
```

## Integration

### With Agent Context
Configure `auto_inject` in `config.yaml`:
```yaml
auto_inject:
  enabled: true
  max_tokens: 5000
  triggers:
    - "income"
    - "skills"
```

### With Cron Manager
```bash
# Weekly memory summary
0 0 * * 0 clawhub memory summarize --output weekly-summary.md
```

### With Inbox Triage
```yaml
# Store triage context automatically
auto_inject:
  triggers:
    - "inbox"
  memories:
    - "inbox-triage skill is complete"
```

## Testing

```bash
# Run test suite
python scripts/memory.py store "Test memory"
python scripts/memory.py search "Test memory"
python scripts/memory.py list
```

## Output Formats

### Markdown (default)
```markdown
### decision (score: 0.92)
**Content:** Published inbox-triage skill  
**Tags:** income, skills  
**Created:** 2026-04-15
```

### JSON
```json
{
  "results": [
    {
      "id": "uuid-123",
      "content": "Published inbox-triage skill",
      "score": 0.92,
      "type": "decision",
      "tags": ["income", "skills"]
    }
  ],
  "total": 1
}
```

## Limitations

- **Token budget:** Context injection respects 48k token ceiling
- **Search accuracy:** Semantic search may miss nuanced queries
- **Privacy:** Do not store sensitive data (passwords, API keys)
- **Local only:** No cloud sync (yet)

## Contributing

1. Fork the repository
2. Improve search scoring algorithm
3. Add encrypted storage for sensitive data
4. Submit PR

## License

MIT - See LICENSE file for details.

---

Built with ❤️ for the OpenClaw ecosystem.
