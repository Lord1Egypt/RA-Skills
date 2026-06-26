# Inbox Triage Skill

> Automate message management by categorizing, summarizing, and drafting responses.

## Quick Start

```bash
# Install via clawhub
npx clawhub install inbox-triage

# Or clone manually
git clone https://clawhub.ai/skills/inbox-triage.git ~/.openclaw/skills/inbox-triage

# Run triage
clawhub run inbox-triage
```

## Features

- ✅ **Auto-categorize** messages as Urgent/Normal/Spam
- ✅ **Daily digest summaries** of all messages
- ✅ **Draft responses** for non-urgent items
- ✅ **Learning mode** - improves from corrections
- ✅ **JSON & Markdown** output formats
- ✅ **Configurable** rules and thresholds

## Usage

### Basic Triage
```bash
python scripts/triage.py \
  --input messages.json \
  --output digest.md \
  --format markdown
```

### Generate Drafts
```bash
python scripts/triage.py \
  --input messages.json \
  --draft-responses \
  --format json
```

### Daily Digest
```bash
clawhub run inbox-triage --daily-digest --output ~/logs/daily-triage-$(date +%Y-%m-%d).md
```

## Configuration

Edit `config.yaml` to customize:
- `sources`: Which message channels to process
- `rules`: Keyword patterns for classification
- `responses`: Draft response templates

Example:
```yaml
sources:
  - type: signal
    enabled: true
  - type: telegram
    enabled: true

rules:
  urgent_keywords:
    - "urgent"
    - "ASAP"
    - "deadline"
```

## Testing

```bash
# Run test suite
python scripts/triage.py --input test_messages.json --output triage_test.md --format markdown

# View results
cat triage_test.md
```

## Integration

### Cron Scheduler
```bash
# Daily digest at 8AM
0 8 * * * cd ~/.openclaw/skills/inbox-triage && python scripts/triage.py --input ~/inbox/messages.json --output ~/logs/daily-triage.md
```

### With Weather Alert
```bash
if weather is-clear; then
  clawhub run inbox-triage --send-summary
fi
```

## Output Format

### Markdown (default)
```markdown
# Daily Inbox Digest - 2026-04-15

🔴 **URGENT** (2):
  - Budget Approval Needed... from Sarah

🟡 **NORMAL** (4):
  - Good work!... from Team Lead

🟢 **SPAM/NOISE** (0): Filtered
```

### JSON (machine-readable)
```json
{
  "timestamp": "2026-04-15T20:37:00Z",
  "urgent": [{"sender": "Sarah", "subject": "Budget Approval"}],
  "normal": [{"sender": "Team", "subject": "Good work"}],
  "spam": [],
  "drafted_responses": []
}
```

## Contributing

1. Fork the repository
2. Make changes and test
3. Add corrections to learn from mistakes
4. Submit PR

## License

MIT - See LICENSE file for details.

## Support

Issues & feature requests: https://github.com/openclaw/skills/issues

---

Built with ❤️ for the OpenClaw ecosystem.
