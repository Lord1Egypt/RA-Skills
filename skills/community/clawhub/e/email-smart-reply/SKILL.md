---
name: email-smart-reply
description: "AI-powered email reply generation for B2B sales. Analyzes incoming emails to detect intent (inquiry, delivery chase, complaint, technical question, partnership, spam), retrieves relevant knowledge base content, generates contextually appropriate draft replies, and routes low-confidence replies for human review via Discord. Use when you need to automate initial email response drafting for sales inquiries."
---

# email-smart-reply

**Category:** Email Automation  
**Status:** Production-Ready  
**Version:** 1.0.0  
**Created:** 2026-03-24  
**Maintainer:** WILSON + IRON

---

## Description

Intelligent email auto-reply pipeline for B2B sales. Automatically classifies incoming emails by intent, retrieves relevant knowledge from your knowledge base, generates personalized reply drafts, and routes them through a Discord-based human review workflow before sending.

**Pipeline:** IMAP fetch → Intent Recognition → KB Retrieval → Reply Generation → Discord Review → SMTP Send

This skill is designed for B2B electronics manufacturing email workflows. It understands product lines (HDMI/DP/USB/LAN cables), customer intent categories specific to electronics manufacturing, and integrates with CRM data.

---

## Core Modules

| File | Purpose |
|------|---------|
| `scripts/intent-recognition.js` | Classifies email intent via LLM (OpenRouter) with keyword fallback |
| `scripts/kb-retrieval.js` | Retrieves relevant knowledge from LanceDB + Obsidian vault |
| `scripts/reply-generation.js` | Generates personalized reply drafts using templates + KB context |
| `scripts/discord-review.js` | Pushes drafts to Discord for human approval before sending |
| `scripts/integration-test.js` | End-to-end pipeline test with `--dry-run` mode |
| `config/intent-schema.json` | Defines 6 intent categories with thresholds and behaviors |
| `config/discord-config.json` | Discord bot token and channel configuration |

---

## Intent Categories

Defined in `config/intent-schema.json`:

| ID | English | Chinese | Priority | Auto-Draft | Fallback |
|----|---------|---------|---------|-----------|---------|
| `inquiry` | Product Inquiry | 产品询价 | high | ✅ | manual_review |
| `delivery-chase` | Delivery Follow-up | 交期催促 | high | ✅ | manual_review |
| `complaint` | Customer Complaint | 客户投诉 | **urgent** | ❌ | escalate_to_human |
| `technical` | Technical Support | 技术支持 | medium | ✅ | manual_review |
| `partnership` | Partnership/Collaboration | 合作意向 | high | ✅ | manual_review |
| `spam` | Spam/Promotional | 垃圾邮件 | low | ❌ | ignore |

**Confidence threshold:** 0.75 (below this → `needs_manual = true`, no auto-draft sent)

---

## Usage

### Run Full Pipeline (Dry Run)
```bash
cd $WORKSPACE/skills/email-smart-reply/scripts
node integration-test.js --dry-run --limit 5
```

### Run Full Pipeline (Live - sends to Discord review)
```bash
node integration-test.js --limit 10
```

### Intent Recognition Only
```javascript
const { recognizeIntent } = require('./scripts/intent-recognition');
const result = await recognizeIntent(emailText);
// Returns: { intent, confidence, method: 'llm'|'keyword' }
```

### KB Retrieval Only
```javascript
const { retrieveKB } = require('./scripts/kb-retrieval');
const results = await retrieveKB({ intent, emailText });
// Returns: { found, results: [{source, content}], queries }
```

### Generate Reply Draft
```javascript
const { generateReply } = require('./scripts/reply-generation');
const draft = await generateReply({ email, intentResult, kbResults });
// Returns: { draft_id, subject, body, needs_manual, reason } or null
// Draft saved to: $WORKSPACE/skills/imap-smtp-email/drafts/
```

### Push to Discord Review
```javascript
const { pushToDiscordReview } = require('./scripts/discord-review');
await pushToDiscordReview({ draft, email, intentResult });
// Sends embed with Approve/Edit/Discard buttons to #email-review channel
```

### Discord Review CLI (manual actions)
```bash
node scripts/discord-review.js test          # Send test embed
node scripts/discord-review.js approve <draft_id>
node scripts/discord-review.js discard <draft_id>
```

---

## Draft ID Format

`DRAFT-{timestamp}-{3-letter-prefix}`

| Intent | Prefix |
|--------|--------|
| inquiry | INQ |
| delivery-chase | DEL |
| complaint | COM |
| technical | TEC |
| partnership | PAR |
| spam | (filtered, no draft) |

---

## Dependencies

### External Services
- **IMAP/SMTP:** Configured email account via enterprise mail provider
- **OpenRouter API:** LLM intent classification (API key in `.env`)
- **Discord Bot:** Token + channel (configured in `config/discord-config.json`)

### Local Skills/Tools
- `$WORKSPACE/skills/imap-smtp-email/` — IMAP/SMTP transport layer
- `$WORKSPACE/vector_store/okki_vector_search_v3.py` — LanceDB vector search
- `$KB_PATH` — Product knowledge base (Obsidian vault)

### Node.js Packages
- `imap` / `nodemailer` — email transport (inherited from imap-smtp-email skill)
- `node-fetch` — OpenRouter API calls
- `discord.js` — Discord bot integration

---

## Configuration

### `config/intent-schema.json`
- Intent definitions, keywords (EN + ZH), confidence thresholds
- Fallback behaviors per intent type
- Global settings (multi-intent handling, language detection)

### `config/discord-config.json`
- `bot_token`: Discord bot token
- `channel_id`: Target channel for review embeds (`<your-discord-channel-id>`)
- `review_timeout_minutes`: Auto-discard timeout (default: 30)

---

## Safety Guarantees

1. **No blind sending:** All drafts require human approval via Discord before SMTP send
2. **Low confidence → manual:** Confidence < 0.75 sets `needs_manual=true`, skips Discord push, queues for manual review
3. **Complaint escalation:** Complaint intent never auto-drafts; always escalates to human
4. **Spam filtering:** Spam intent immediately discarded, no draft created
5. **Dry-run mode:** `--dry-run` flag for safe testing without real sends or Discord posts
6. **Fallback degradation:** LLM unavailable → keyword matching; IMAP unavailable → sample emails

---

## Development History

**Task:** task-001 | **Phase:** 1 | **Iterations:** 5 | **Duration:** ~2.5 hours

| Iteration | Agent | What Was Built |
|-----------|-------|----------------|
| 1 | IRON | Initial attempt (timed out at 300s — restructured to single-subtask iterations) |
| 2 | IRON | Steps 1-3: intent-schema.json, intent-recognition.js, kb-retrieval.js |
| 3 | IRON | Step 4: reply-generation.js (templates, escalation logic, draft file I/O) |
| 4 | IRON | Step 5: discord-review.js (Embed format, 3-button interaction, CLI fallback) |
| 5 | IRON | Step 6: integration-test.js (full pipeline, --dry-run, test-results/ output) |

**Key Design Decisions:**
- Single-subtask-per-iteration strategy after initial timeout failure
- LLM → keyword cascade for intent recognition robustness
- Discord embed review (not email approval) for fast human-in-the-loop UX
- `needs_manual` flag as primary safety gate (not confidence threshold alone)
- Reviews stored locally in `reviews-pending/` as fallback if Discord is unavailable

**Known Limitations (Phase 1):**
- Integration tests use sample emails (real IMAP auth was unavailable in test env)
- LLM intent classification falls back to keyword matching (confidence ~0.4–0.6)
- Discord live push not tested in dry-run (separately verified in Iteration 4)

---

## Phase 2 Roadmap

1. **Real IMAP testing** — Run pipeline against actual incoming emails, measure intent accuracy
2. **LLM availability** — Ensure OpenRouter API accessible in production
3. **Discord Bot permissions** — Confirm bot has send access to `#email-review` channel
4. **Cron job** — Schedule `integration-test.js` every 30 minutes via cron
5. **Manual queue monitoring** — Alert when `needs_manual` backlog exceeds threshold

---

## File Structure

```
email-smart-reply/
├── SKILL.md                    ← This file
├── README.md                   ← Quick start guide
├── scripts/
│   ├── intent-recognition.js   ← LLM + keyword intent classifier
│   ├── kb-retrieval.js         ← LanceDB + Obsidian knowledge retrieval
│   ├── reply-generation.js     ← Template-based reply drafts
│   ├── discord-review.js       ← Discord embed review workflow
│   └── integration-test.js     ← End-to-end pipeline runner
├── config/
│   ├── intent-schema.json      ← Intent categories and thresholds
│   └── discord-config.json     ← Discord bot configuration
└── drafts/                     ← Generated draft replies (gitignored)
```

---

## Environment Variables

Create a `.env` file in the skill root:

```bash
# LLM API
OPENROUTER_API_KEY=your-openrouter-api-key

# Knowledge Base Path (e.g. Obsidian vault)
KB_PATH=/path/to/your/knowledge-base

# Draft output directory
DRAFTS_DIR=./drafts

# Discord Review (optional)
DISCORD_BOT_TOKEN=your-discord-bot-token
DISCORD_REVIEW_CHANNEL_ID=your-channel-id

# IMAP (to read incoming emails)
IMAP_HOST=imap.your-provider.com
IMAP_PORT=993
IMAP_USER=your@email.com
IMAP_PASS=your-password
```

---

## Source

This skill is a **packaged, documented, reusable version** of the email automation pipeline.
