---
name: email-summarizer
description: Email summary and contact profiling skill. Fetch emails from an IMAP mailbox or parse local exports (.pst / .mbox / .msg), build a contact profile report (HTML + Excel), and optionally send it via email. Trigger when user says "summarize my emails", "check recent emails", "analyze my contacts", "profile email contacts", "parse pst file", "analyze outlook export", "send contact report", etc.

# Runtime dependencies
# Python (pip install -r requirements.txt):
#   extract-msg>=0.52.0   — .msg file parsing
#   openpyxl>=3.1.0       — Excel report generation
#
# Node.js (cd scripts && npm install):
#   pst-extractor>=1.10.0 — native .pst parsing (bundled via package.json)
#
# System tools (optional):
#   readpst               — alternative .pst engine (apt install pst-utils / brew install libpst)
#   node >= 16            — required for native PST parsing

# External process usage (declared for security review):
#
#   parse_file.py invokes TWO local executables via subprocess — no shell=True,
#   no dynamic command construction, no network access:
#
#   1. node scripts/pst_extractor_helper.js <pst_file> [--since] [--until] [--max]
#      Calls the Node.js script bundled in this skill's scripts/ directory.
#      Used only when --pst is passed and engine is 'native' (default).
#      node binary is resolved from NODE_BIN env var or system PATH.
#
#   2. readpst -o <tmp_dir> -M <pst_file>
#      Calls the system-installed readpst binary (from pst-utils package).
#      Used only when --pst-engine readpst is explicitly requested.
#      Both executables accept only local file paths — no URLs, no user shell input.

# Credentials (only needed for IMAP fetch and SMTP send; local file parsing needs none)
env:
  EMAIL_USER:
    description: Your email address. Used for IMAP login and SMTP sender.
    required: false
    example: "you@163.com"
  EMAIL_PASS:
    description: IMAP/SMTP app password (NOT your login password). Generate in mailbox settings under POP3/SMTP/IMAP.
    required: false
    example: "your-app-password"
---

# Email Summarizer + Contact Profiler

Three independent stages — run any subset depending on what you need:

```
[Data Source]          [Analysis]          [Delivery]
fetch_imap.py    ──→                ──→
parse_file.py    ──→  build_report.py ──→  send_report.py
                       → .html + .xlsx
```

Each stage reads from / writes to files (or stdin/stdout), so they compose freely.

---

## Installation

```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependency (only for native .pst parsing)
cd scripts && npm install && cd ..
```

---

## Script Reference

### Stage 1 — Data Source

#### `fetch_imap.py` — Fetch emails from a live IMAP mailbox

```bash
export EMAIL_USER=you@163.com
export EMAIL_PASS=your-app-password

# Fetch last 7 days (inbox only) → emails.json
python3 scripts/fetch_imap.py --days 7 --output emails.json

# Fetch a date range, inbox + sent
python3 scripts/fetch_imap.py --since 2026-03-01 --until 2026-03-28 \
    --with-sent --preset 163 --output emails.json

# Pipe directly to build_report.py (no intermediate file)
python3 scripts/fetch_imap.py --days 30 | python3 scripts/build_report.py --output report
```

| Flag | Default | Description |
|------|---------|-------------|
| `--days N` | 7 | Fetch last N days. Ignored if `--since` is set. |
| `--since DATE` | — | Start date inclusive (YYYY-MM-DD) |
| `--until DATE` | — | End date exclusive (YYYY-MM-DD, default: today) |
| `--max N` | 200 | Max emails per folder |
| `--folder NAME` | INBOX | Inbox folder name |
| `--preset NAME` | 163 | Mailbox preset: `163` \| `qq` \| `exmail` \| `gmail` \| `outlook` |
| `--with-sent` | off | Also fetch Sent folder (recommended for relationship analysis) |
| `--output FILE` | stdout | Write JSON to file; prints to stdout if omitted |

Supported presets:

| Preset | IMAP Server | Sent folder |
|--------|-------------|-------------|
| `163` | imap.163.com:993 | 已发送 |
| `qq` | imap.qq.com:993 | Sent Messages |
| `exmail` | imap.exmail.qq.com:993 | Sent Messages |
| `gmail` | imap.gmail.com:993 | [Gmail]/Sent Mail |
| `outlook` | outlook.office365.com:993 | Sent Items |

---

#### `parse_file.py` — Parse a local email export

```bash
# Parse a .pst file (native engine, no system install needed)
python3 scripts/parse_file.py --pst ~/Downloads/archive.pst --output emails.json

# Parse a .mbox file (inbox + sent)
python3 scripts/parse_file.py --mbox Inbox.mbox --sent-mbox Sent.mbox --output emails.json

# Parse a folder of .msg files, filter by date
python3 scripts/parse_file.py --msg-dir ./exported/ --since 2026-01-01 --output emails.json

# Pipe to build_report.py
python3 scripts/parse_file.py --pst archive.pst | python3 scripts/build_report.py --output report
```

| Flag | Default | Description |
|------|---------|-------------|
| `--pst FILE` | — | Outlook .pst archive |
| `--mbox FILE` | — | Unix mbox file |
| `--msg-dir DIR` | — | Folder of .msg files |
| `--sent-mbox FILE` | — | Additional sent-items mbox (with `--mbox`) |
| `--pst-engine` | auto | `auto` \| `native` \| `readpst` |
| `--days N` | all | Only include last N days |
| `--since DATE` | — | Start date inclusive (YYYY-MM-DD) |
| `--until DATE` | — | End date exclusive (YYYY-MM-DD) |
| `--max N` | 500 | Max emails to load |
| `--output FILE` | stdout | Write JSON to file; prints to stdout if omitted |

PST engines:

| Engine | Flag | Requires |
|--------|------|----------|
| Native (default) | `--pst-engine native` | `cd scripts && npm install` |
| Readpst | `--pst-engine readpst` | `apt install pst-utils` or `brew install libpst` |
| Auto | `--pst-engine auto` | Tries native first, falls back to readpst |

---

### Stage 2 — Analysis

#### `build_report.py` — Analyse emails → HTML + Excel report

```bash
# From a file
python3 scripts/build_report.py --input emails.json --output report

# Specify owner explicitly (when analysing someone else's PST)
python3 scripts/build_report.py --input emails.json --output report \
    --owner xiang-xiang.hu@connect.polyu.hk

# From stdin (piped from Stage 1)
python3 scripts/fetch_imap.py --days 30 | python3 scripts/build_report.py --output report
```

| Flag | Default | Description |
|------|---------|-------------|
| `--input FILE` | stdin | Path to emails JSON from Stage 1 |
| `--output PREFIX` | contact_report | Output path prefix. Writes `<prefix>.html` and `<prefix>.xlsx` |
| `--owner EMAIL` | auto-inferred | Mailbox owner address. Auto-detected if omitted. |

Output files:
- `<prefix>.html` — self-contained HTML report (open in browser or attach to email)
- `<prefix>.xlsx` — Excel spreadsheet with the same data

Report columns: `#` / `Preferred Name` / `Email` / `Company` / `Position` / `Subject Summary` / `Source` / `Emails (Recv/Sent)`

---

### Stage 3 — Delivery

#### `send_report.py` — Send report files via SMTP

```bash
export EMAIL_USER=you@163.com
export EMAIL_PASS=your-app-password

# Send HTML + Excel to a recipient
python3 scripts/send_report.py \
    --html report.html --xlsx report.xlsx --to friend@example.com

# Send to yourself (EMAIL_USER)
python3 scripts/send_report.py --html report.html --xlsx report.xlsx

# HTML only (no attachment)
python3 scripts/send_report.py --html report.html --to friend@example.com

# Custom subject
python3 scripts/send_report.py --html report.html --subject "March Contact Report"
```

| Flag | Default | Description |
|------|---------|-------------|
| `--html FILE` | required | HTML file to use as email body |
| `--xlsx FILE` | — | Excel file to attach (optional) |
| `--to ADDR` | EMAIL_USER | Recipient address |
| `--subject STR` | auto | Email subject (auto-generated if omitted) |
| `--preset NAME` | 163 | SMTP preset: `163` \| `qq` \| `exmail` \| `gmail` \| `outlook` |

---

## Private library modules (not standalone scripts)

| File | Provides |
|------|----------|
| `_core.py` | `decode_header`, `parse_addr`, `get_domain`, `strip_html`, `html_esc`, `get_body` |
| `_analyze.py` | `infer_owner`, `build_contacts`, domain/company/position/name inference |
| `_render.py` | `build_report_html`, `build_excel`, `SMTP_MAP` |

---

## Complete workflow examples

### A — IMAP mailbox → report → send to self

```bash
export EMAIL_USER=you@163.com
export EMAIL_PASS=your-app-password

python3 scripts/fetch_imap.py --days 30 --with-sent --output /tmp/emails.json
python3 scripts/build_report.py --input /tmp/emails.json --output /tmp/report
python3 scripts/send_report.py --html /tmp/report.html --xlsx /tmp/report.xlsx --preset 163
```

### B — PST file → report → send to someone

```bash
python3 scripts/parse_file.py --pst ~/Downloads/archive.pst --output /tmp/emails.json
python3 scripts/build_report.py --input /tmp/emails.json --output /tmp/report
EMAIL_USER=sender@163.com EMAIL_PASS=xxx \
  python3 scripts/send_report.py --html /tmp/report.html --xlsx /tmp/report.xlsx \
    --to recipient@example.com
```

### C — One-liner (pipe, no intermediate files)

```bash
python3 scripts/parse_file.py --pst archive.pst \
  | python3 scripts/build_report.py --output /tmp/report
```

### D — Report only, no email (open locally)

```bash
python3 scripts/parse_file.py --mbox Inbox.mbox --output /tmp/emails.json
python3 scripts/build_report.py --input /tmp/emails.json --output /tmp/report
# Open /tmp/report.html in a browser
```

---

## AI analysis templates

After loading the email JSON into the AI context, use the following templates:

### Part A: 4-Dimension Email Summary

```
🔥 Part 1 — Important & Action Items
  🚨 [URGENT]    Subject — Sender — Date | Summary | Action | Deadline
  ⚡ [IMPORTANT] Subject — Sender — Date | Summary | Action
  📌 [NOTE]      Subject — Sender — Date | Summary

📊 Part 2 — Grouped by Sender / Topic

✅ Part 3 — To-Do List

📅 Part 4 — Timeline (YYYY-MM-DD  Sender → Subject: summary)
```

### Part B: Contact Profile Analysis

Sort by total interactions. For each contact:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Rank #N | Name <email>   Total: N (Recv: N / Sent: N)
🧑 Gender       M/F/Unknown  Confidence: H/M/L  Basis: …
💼 Role         …            Basis: domain / signature / keywords
🔗 Relationship Colleague / Client / Institution / Stranger
   Direction    Mutual / Owner-initiated / Contact-initiated
📝 Topics       • subject 1  • subject 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Heat scale: 🔥 Heavy (≥10) · ⚡ Active (5–9) · 💬 Moderate (2–4) · 🌙 Light (1)

---

## Notes

- Credentials are passed via environment variables — never hardcoded
- IMAP connections use readonly mode — emails are never modified or deleted
- Body text is truncated to 2000 characters per email
- `fetch_imap.py` sends an RFC 2971 ID command required by 163/188 servers; harmless on others
