---
name: flashrev-notion-tracker
description: Use this skill whenever emails are sent or dry-run previewed via the flashrev-mailer CLI and you need to log, track, or audit those emails in Notion. Triggers on requests to log sent emails to Notion, track flashrev campaign sends, record email history, audit outreach campaigns, or view and query past sends. Always invoke after a flashrev-mailer send or dry-run step completes. Also use when the user asks to check what emails were sent, view campaign logs in Notion, or search past outreach.
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - node
      config:
        - NOTION_TOKEN
        - NOTION_DATABASE_ID
---

# FlashRev Notion Email Tracker

Pushes every `flashrev-mailer` send attempt into your Notion database using the Notion API directly. Reads `NOTION_TOKEN` and `NOTION_DATABASE_ID` from OpenClaw config — no MCP, no extra setup beyond those two values.

---

## One-time setup

The user must add two values in OpenClaw settings before the skill works:

**`NOTION_TOKEN`**
Notion → Settings → Connections → Develop or manage integrations → New integration → copy the Internal Integration Secret.

**`NOTION_DATABASE_ID`**
Open your target Notion database → Share → Copy link → grab the 32-char ID from the URL:
`notion.so/workspace/`**`abc123...`**`?v=...`

Then share the database with the integration: open the database → `...` menu → Add connections → select your integration.

---

## Running the tracker

### Step 1 — Install dependencies (first use only)
```bash
cd scripts && npm install && cd ..
```

### Step 2 — Push after every send batch
After each `flashrev-mailer send` or `--dry-run` completes, run:
```bash
node scripts/notion-push.js --campaign CAMPAIGN_ID
```
Use the exact `--campaign` slug from `flashrev-mailer` (e.g. `launch-001`).

### Step 3 — Read the output and report to user
```
🔗 Connected to Notion database: FlashRev Tracker
📂 Loaded 48 entries (campaign: launch-001)
🔍 Deduplication: 2 already exist, 46 new
✓ Batch 1 / 5 — 10 written
...
✅ Done. 46 written · 2 skipped (dup) · 0 errors
🔗 https://notion.so/abc123...
```

### Query without writing
```bash
node scripts/notion-push.js --campaign CAMPAIGN_ID --query-only
```

---

## Integration sequence with flashrev-mailer

```
1. flashrev-mailer  →  send --campaign X --limit 10 --dry-run --yes
2. this skill       →  node scripts/notion-push.js --campaign X
3. user approves live send
4. flashrev-mailer  →  send --campaign X --limit 10 --live --yes
5. this skill       →  node scripts/notion-push.js --campaign X
6. repeat 4-5 for each approved batch
```

---

## Error messages

| Script output                        | Tell the user                                                        |
|--------------------------------------|----------------------------------------------------------------------|
| `NOTION_TOKEN is not set`            | Add NOTION_TOKEN in OpenClaw settings                                |
| `NOTION_DATABASE_ID is not set`      | Add NOTION_DATABASE_ID in OpenClaw settings                          |
| `Could not find send-log`            | flashrev-mailer send has not completed yet — check the CLI output    |
| `API token is invalid`               | NOTION_TOKEN is wrong or expired — regenerate it in Notion           |
| `Could not find database`            | NOTION_DATABASE_ID is wrong, or integration not shared with database |
| `Property does not exist`            | Database is missing a column — add it manually in Notion             |

---

## What gets logged (11 fields per email)

Name · Recipient Email · Subject Line · Body Preview (300 chars) · Campaign ID · Send Timestamp · Validation Status · Sender Mailbox · Send Mode · Send Result · Error Detail