---
name: registration-scanner
description: Scans email accounts (Gmail, iCloud, Outlook, Yahoo, AOL, GMX, Web.de, Fastmail, Proton, T-Online and more) for registration, welcome and confirmation emails to build a chronological list of all services the user has ever signed up for. Triggers on phrases like "where am I registered", "scan my email for registrations", "show me all my accounts", "welche dienste habe ich", "wo bin ich registriert", "liste mes inscriptions", "encuentra mis registros".
user-invocable: true
metadata: {"openclaw":{"emoji":"📋","always":false}}
---

# Registration Scanner

Scans one or more email accounts for registration-related emails and returns a deduplicated, date-sorted list of every service the user has ever signed up for.

## Supported Providers

| Provider | Access Method |
|---|---|
| Gmail | Gmail tool / MCP connector |
| iCloud Mail | IMAP – imap.mail.me.com:993 |
| Outlook / Hotmail / Live | IMAP – outlook.office365.com:993 |
| Yahoo Mail | IMAP – imap.mail.yahoo.com:993 |
| AOL Mail | IMAP – imap.aol.com:993 |
| GMX | IMAP – imap.gmx.net:993 |
| Web.de | IMAP – imap.web.de:993 |
| T-Online | IMAP – secureimap.t-online.de:993 |
| Fastmail | IMAP – imap.fastmail.com:993 |
| Proton Mail | IMAP Bridge – 127.0.0.1:1143 (Bridge required) |

Full provider details and IMAP setup guides → `{baseDir}/references/providers.md`

---

## Step 1 – Identify Accounts

Ask the user which email accounts to scan before doing anything else:

> "Which email accounts should I scan? (e.g. Gmail, iCloud, Outlook, Yahoo, AOL, GMX, Web.de, T-Online, Fastmail, Proton – or all of them?)"

Wait for the answer. Do not proceed until the user has confirmed.

---

## Step 2 – Collect Credentials

### Gmail
Use the Gmail tool or Gmail MCP connector if already configured.  
If not configured, tell the user:
> "Please connect your Gmail account first via `openclaw configure` or by enabling the Gmail MCP connector."

### IMAP Providers (iCloud, Outlook, Yahoo, AOL, GMX, Web.de, T-Online, Fastmail)
Explain to the user:
> "For [provider] I need your email address and an **app-specific password** (not your regular login password). You can generate one in your account's security settings. I will use it only for this session and never store it in plain text."

Refer to provider-specific instructions for generating app passwords → `{baseDir}/references/providers.md`

### Proton Mail
Proton Mail requires the **Proton Mail Bridge** to be running locally.  
> "For Proton Mail, please make sure the Proton Mail Bridge is running. I will connect to it locally at 127.0.0.1:1143."

---

## Step 3 – Run the Scan

### Gmail
Use the Gmail tool to search with these queries in sequence. Collect all matching message IDs.

Search queries across all languages → `{baseDir}/references/search-queries.md`

### IMAP Accounts
Use the Python script at `{baseDir}/scripts/imap_scan.py` to connect and search:

```bash
python3 "{baseDir}/scripts/imap_scan.py" \
  --host "imap.mail.me.com" \
  --port 993 \
  --user "user@icloud.com" \
  --password "app-specific-password" \
  --output "/tmp/registration_scan_results.json"
```

The script runs all search query batches automatically and returns a JSON list of matches.

Run this for each IMAP account separately, saving results to different temp files.

---

## Step 4 – Parse and Deduplicate Results

For every matched email:

1. Extract: `From`, `Date`, `Subject`
2. Derive the **service name** from the sender domain or subject line  
   Example: `noreply@spotify.com` → `Spotify`, `hello@notion.so` → `Notion`
3. **Deduplicate by service**: keep only the **oldest** entry per service (= original registration)
4. **Skip**: transactional emails (password resets, receipts), pure newsletters with no registration context, internal/personal senders

---

## Step 5 – Output

Present the final list sorted **newest first**. Use this format:

```
📋 REGISTERED SERVICES – [Account Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found: XX services  |  Range: YYYY – YYYY

YYYY-MM-DD   Service Name
             From: sender@domain.com

YYYY-MM-DD   Service Name
             From: sender@domain.com
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If multiple accounts were scanned, merge all results into one unified list sorted by date.

After showing the list, ask:
> "Should I save this as a file? Or filter by a specific service or date range?"

---

## Error Handling

- **IMAP auth failure**: Ask the user to re-check their app password. Refer to `{baseDir}/references/providers.md` for setup steps.
- **IMAP not enabled**: iCloud, Yahoo, Outlook may require IMAP to be turned on in account settings. Provider guide → `{baseDir}/references/providers.md`
- **Proton Bridge not running**: Instruct the user to start the Proton Mail Bridge app first.
- **Rate limiting**: Pause 1–2 seconds between search batches to avoid being throttled.
- **Large mailbox**: Inform the user of progress. Large inboxes (100k+ emails) may take several minutes.

---

## Privacy & Security Rules

- **Never** display passwords, app keys, or credentials in output or logs.
- Use OpenClaw's Secret Store for credentials whenever possible.
- Delete temp files (`/tmp/registration_scan_*.json`) after the session ends.
- Do not send any email content to external services.
