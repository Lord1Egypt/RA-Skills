# Email Checker by EntzAI

An automated email assistant for Apple Mail on macOS. Runs on a schedule,
scores your unread emails by priority, drafts AI replies, and sends you a
report — so you can manage your inbox from Telegram or WhatsApp without ever
opening Mail.app.

> **Requires:** macOS · Python 3 · Mail.app · Optional: local or remote LLM

---

## How It Works

1. Runs on a schedule (hourly by default, fully configurable)
2. Fetches unread emails from your Mail.app INBOX
3. Scores each email **HIGH / MEDIUM / LOW** based on keywords and trusted senders
4. Drafts a contextual AI reply for each email (or skips if LLM is disabled)
5. Emails you a report with previews and draft replies
6. Marks processed emails as read

---

## Use Cases

### The OpenClaw Setup _(recommended)_

This is the workflow the app was designed for:

- You have a **dedicated machine or VM running OpenClaw** (your AI assistant)
- That machine has its own **bot email account** in Mail.app — this is the inbox it watches
- Email Checker runs on that machine **every hour via cron**
- When emails arrive: checker scores them, drafts replies, and **sends a report to your personal email**
- You read the report on your phone — you see each email's priority, a preview, and an AI-drafted reply
- If you like a draft, you tell OpenClaw via **Telegram or WhatsApp**: _"Send that reply to Angelo"_
- **You never open the bot's inbox.** The whole flow lives in your phone's chat

This works great on macOS Tahoe (26.3) on Apple Silicon with OpenClaw as your always-on assistant.

### Personal Productivity

- Run on your main Mac, connected to your own Mail.app account
- Get hourly digest reports with AI-drafted replies in your inbox
- Review and approve drafts without context-switching into Mail.app
- Send replies via `send_reply.py` or by telling OpenClaw

### Low-Tech Mode _(no LLM)_

- Set `"provider": "none"` in `settings.json`
- Still scores and previews every unread email by priority
- Report shows subject, sender, preview — no AI drafts
- Useful for a smart email digest with zero LLM dependency

---

## Quick Start

### 1. Prerequisites

- macOS (tested on Tahoe 26.3, Apple Silicon)
- Python 3 — `brew install python` if missing
- Mail.app configured with at least one account

### 2. Get the project

```bash
git clone https://github.com/entzclaw/email-checker-for-mac
cd email-checker-for-mac
```

### 3. Run setup

```bash
bash setup.sh
```

The wizard will:
- Auto-discover your Mail.app accounts — pick yours from a numbered list
- Prompt for your name, bot name, report destination email, and trusted senders
- Let you pick an LLM provider (LM Studio, Ollama, OpenAI, or skip)
- Test the LLM connection before saving
- Write `config/settings.json` (gitignored — never leaves your machine)
- Optionally install the crontab and run a first test

### 4. Grant Mail.app permissions

**System Settings → Privacy & Security → Automation**
→ Allow **Terminal** to control **Mail**

If cron jobs fail, also add Terminal under **Full Disk Access**.

### 5. Test

```bash
python3 scripts/email/checker.py
```

---

## Configuration

All config lives in `config/settings.json` — created by `setup.sh`, gitignored.
See `config/settings.example.json` for the full structure.

### Trusted Senders

Trusted senders get a **+2 priority score boost**. Each entry is matched as a
**case-insensitive substring** of the sender's full `From:` field.

The `From:` field contains both the display name and address, e.g.:
```
Alice Smith <alice@company.com>
```

| Entry | What it matches | Use when |
|---|---|---|
| `"Alice"` | Display name (partial) | You know their first name |
| `"@company.com"` | Everyone from a domain | Trust a whole organisation |
| `"alice@example.com"` | That exact address only | Specific person, any display name |

**Example:**
```json
"trusted_senders": ["Alice", "bob", "@mycompany.com", "ceo@bigcorp.com"]
```

You can update this list by:
- Editing `config/settings.json` directly, or
- Telling OpenClaw via Telegram/WhatsApp: _"Add sarah@example.com to trusted senders"_

### LLM Providers

| Provider | `provider` | `base_url` | Notes |
|---|---|---|---|
| LM Studio | `lm_studio` | Your LM Studio URL | Local or remote vLLM |
| Ollama | `ollama` | `http://localhost:11434/v1` | Local, set by setup.sh |
| OpenAI | `openai` | `https://api.openai.com/v1` | Requires API key |
| Disabled | `none` | — | Reports without drafts |

### Cron Schedule

Default: every hour. Change by editing crontab (`crontab -e`):

```
# Every hour (default)
0 * * * * /abs/path/to/scripts/email/checker_wrapper.sh

# Every 30 minutes
*/30 * * * * /abs/path/to/scripts/email/checker_wrapper.sh

# Every 5 minutes
*/5 * * * * /abs/path/to/scripts/email/checker_wrapper.sh
```

Re-run `bash setup.sh` to reinstall crontab with updated paths if you move the folder.

---

## Working with OpenClaw

If you're running OpenClaw as your AI assistant, this app integrates naturally
via Telegram or WhatsApp:

**Update config:**
> _"Add @newcompany.com to my trusted senders"_
> _"Change my report email to myphone@example.com"_
> _"Switch the LLM model to gpt-4o"_

OpenClaw edits `config/settings.json` directly — changes take effect on the next run.

**Send a reply:**
> _"Send the draft reply to Angelo"_
> _"Reply to the GitHub notification with: noted, reviewing tomorrow"_

```bash
python3 scripts/email/send_reply.py \
    --to colleague@example.com \
    --subject "Re: Something" \
    --content "Your reply here"

# From a file
python3 scripts/email/send_reply.py \
    --to someone@example.com \
    --subject "Re: Something" \
    --file /path/to/draft.txt
```

**Trigger a manual check:**
> _"Run the email checker now"_

```bash
python3 scripts/email/checker.py
```

**Check logs:**
```bash
tail -f logs/email_check.log
```

---

## Directory Structure

```
email-checker-for-mac/
├── README.md
├── setup.sh                           # Interactive setup wizard
├── _meta.json                         # ClawHub metadata
├── config/
│   ├── settings.example.json          # Template (committed to git)
│   ├── settings.json                  # Your config (gitignored)
│   └── email_check_crontab.txt        # Cron reference (written by setup.sh)
├── scripts/
│   └── email/
│       ├── checker.py                 # Main email checker
│       ├── checker_wrapper.sh         # Cron entry point — owns logging
│       ├── get_unread_emails.scpt     # AppleScript: fetch unread emails
│       └── send_reply.py             # Manual / OpenClaw reply sender
├── logs/                              # Runtime logs (gitignored)
└── temp/                              # Runtime cache (gitignored)
```

---

## Troubleshooting

**"Config not found. Run setup.sh first."**
Run `bash setup.sh` — it walks you through everything.

**"Not authorized to send Apple events to Mail"**
System Settings → Privacy & Security → Automation → Allow Terminal to control Mail.
If using cron, also add Terminal to Full Disk Access.

**LLM times out or connection failed**
The model may still be processing a previous request server-side. Wait 1–2 minutes.
Increase `"timeout"` in `settings.json` for slow models.

**Wrong account / no emails detected**
Re-run `bash setup.sh` — it lists all Mail.app accounts for you to pick from.

**Logs not writing**
```bash
chmod +x scripts/email/checker_wrapper.sh
```

---

---

## Changelog

### v1.1.1 — 2026-03-24

**Setup wizard hotfix**
- LLM test now prints "please wait up to 15 seconds" — so users don't press Enter while waiting
- Flush buffered stdin before the "Continue anyway?" prompt — prevents a stray Enter from auto-accepting
- Changed "Continue anyway?" default from N (abort) to Y (continue) — LLM being offline shouldn't block the whole setup

### v1.1.0 — 2026-03-24

**Setup wizard improvements**
- Removed `set -e` — wizard no longer quits silently on any non-zero exit
- Required fields (name, email, model ID) now loop until valid — blank input re-prompts instead of saving empty values
- Email address format validated before saving
- LLM test captures both stdout and stderr — shows specific error (`CONNECTION_ERROR`, `HTTP_ERROR 401/404/400`) instead of a blank failure message
- If LLM test fails, user is asked whether to continue or abort
- Settings write is verified — exits with a clear error if `settings.json` fails to write
- All Y/N prompts loop until valid input, with sensible defaults
- Final success screen prints a summary: config path, schedule, report email, LLM model

**Priority & drafts**
- AI draft replies are now generated only for **HIGH** priority emails
- MEDIUM and LOW emails show a preview only — faster and uses less LLM

**Subject deduplication**
- Thread subject normalisation now strips nested prefixes (`Re: Re: Re:`, `Fwd: Re:`)
- Strips bracket tags (`[EXTERNAL]`, `[BULK]`) before comparing subjects
- Strips trailing punctuation and symbols

### v1.0.0 — 2026-03-02

Initial release.

- Automated inbox scanning via AppleScript and Mail.app
- Priority scoring (HIGH / MEDIUM / LOW) with trusted sender boost
- AI draft replies via LM Studio, Ollama, or OpenAI
- Hourly email report sent to your personal address
- Interactive setup wizard with crontab installer
- Published to ClawHub as `email-checker-by-entzai`

---

_Built by EntzAI · Powered by OpenClaw_
