# Email Smart Reply — Quick Start

Intelligent email auto-reply pipeline for B2B sales.

## What It Does

1. **Fetch** incoming emails via IMAP
2. **Classify** intent (inquiry / delivery / complaint / technical / partnership / spam)
3. **Retrieve** relevant knowledge from your KB + CRM
4. **Generate** personalized reply draft
5. **Review** via Discord embed (Approve / Edit / Discard)
6. **Send** via SMTP (only after approval)

## Quick Start

### 1. Prerequisites

Ensure these are configured:

```bash
# IMAP/SMTP credentials
cat $WORKSPACE/skills/imap-smtp-email/.env

# Discord bot config
cat config/discord-config.json
```

### 2. Test the Pipeline (Safe — No Real Sends)

```bash
cd scripts
node integration-test.js --dry-run --limit 5
```

Results are saved to `test-results/integration-test-{timestamp}.json`.

### 3. Run Live (Sends to Discord for Review)

```bash
node integration-test.js --limit 10
```

This will:
- Fetch up to 10 unseen emails from IMAP
- Process each through the full pipeline
- Push high-confidence drafts to Discord `#email-review` channel
- Queue low-confidence emails for manual review

### 4. Review and Send via Discord

In the `#email-review` Discord channel, each draft appears as an embed with:
- **✅ Approve & Send** — Sends immediately via SMTP
- **✏️ Edit Draft** — Opens the draft file for editing
- **🗑️ Discard** — Discards the draft

## Configuration

### Intent Thresholds (`config/intent-schema.json`)

| Setting | Default | Notes |
|---------|---------|-------|
| `confidence_threshold` | 0.75 | Below this → manual review |
| `low_confidence_threshold` | 0.5 | Below this → skip Discord, queue manually |

### Discord (`config/discord-config.json`)

```json
{
  "channel_id": "<your-discord-channel-id>",
  "review_timeout_minutes": 30
}
```

## Module Reference

### intent-recognition.js
```javascript
const { recognizeIntent } = require('./intent-recognition');
const result = await recognizeIntent("I need a quote for HDMI 2.1 cables");
// → { intent: 'inquiry', confidence: 0.9, method: 'llm' }
```

### kb-retrieval.js
```javascript
const { retrieveKB } = require('./kb-retrieval');
const kb = await retrieveKB({ intent: 'inquiry', emailText: '...' });
// → { found: true, results: [...], queries: [...] }
```

### reply-generation.js
```javascript
const { generateReply } = require('./reply-generation');
const draft = await generateReply({ email, intentResult, kbResults });
// → { draft_id: 'DRAFT-1711234567-INQ', subject, body, needs_manual: false }
// Draft file saved to: $WORKSPACE/skills/imap-smtp-email/drafts/
```

### discord-review.js
```javascript
const { pushToDiscordReview } = require('./discord-review');
await pushToDiscordReview({ draft, email, intentResult });
```

## Cron Setup (Phase 2)

```bash
# Add to crontab: check every 30 minutes
*/30 * * * * cd $WORKSPACE/skills/email-smart-reply/scripts && node integration-test.js --limit 20 >> /tmp/email-smart-reply.log 2>&1
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| IMAP connection fails | Check `.env` in `imap-smtp-email/`; pipeline auto-falls back to sample emails |
| LLM returns low confidence | OpenRouter API may be unavailable; keyword fallback activates automatically |
| Discord embed not appearing | Check bot token and channel permissions in `config/discord-config.json` |
| All emails flagged `needs_manual` | Confidence < 0.75; LLM may be offline or intent signals are weak |

## Safety Notes

- ❗ **Never runs unattended sends** — all drafts require Discord approval
- ✅ Use `--dry-run` for testing; no Discord messages or emails are sent
- 🚨 Complaints are never auto-drafted; always escalated to human
- 🗑️ Spam is silently discarded

## Source Directory

Active scripts live in:
```
$WORKSPACE/skills/imap-smtp-email/
```

This `email-smart-reply/` directory is the **packaged, documented copy**.
