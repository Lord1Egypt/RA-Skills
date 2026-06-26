---
name: 126mail-cleanup
description: "Use this skill when the user wants to clean up, back up, or optimize their 126.com (NetEase) email account. Covers local backup, spam/subscription bulk deletion, and large attachment stripping. Commands: /126mail backup, classify, cleanup, strip, status."
version: 1.0.0
license: MIT
metadata:
  openclaw:
    emoji: "📧"
    requires:
      bins:
        - python3
      env:
        - MAIL126_ADDRESS
        - MAIL126_AUTH_CODE
      config:
        - name: MAIL126_ADDRESS
          description: "Your 126.com email address (e.g. user@126.com)"
          required: true
        - name: MAIL126_AUTH_CODE
          description: "126 IMAP authorization code (NOT your login password — generate at mail.126.com Settings > POP3/SMTP/IMAP > Authorization Code)"
          required: true
        - name: MAIL126_BACKUP_DIR
          description: "Local directory to store email backups"
          default: "~/Desktop/126mail"
          required: false
        - name: MAIL126_SIZE_THRESHOLD_MB
          description: "Threshold in MB for large attachment detection"
          default: "50"
          required: false
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# 126 Mail Cleanup

A step-by-step assistant for cleaning up, backing up, and optimizing your NetEase 126.com email account via IMAP. Designed to help reclaim cloud storage, reduce clutter, and create a reliable local archive.

## Why Use This Skill

- **Local backup**: Download all emails and attachments to your machine — you own your data, not the cloud
- **Cloud storage savings**: 126 free accounts have limited space (typically 3-5GB); stripping large attachments can reclaim gigabytes, avoiding the need to pay for premium storage
- **Inbox hygiene**: Bulk-delete years of accumulated ads, subscriptions, and platform notifications while preserving important personal emails
- **Safety first**: Every destructive operation has a preview, confirmation, and backup step — nothing is permanently deleted without your approval

## Commands

| Command | Description |
|---------|-------------|
| `/126mail setup` | Configure IMAP credentials and verify connection |
| `/126mail backup` | Download emails to local storage (supports resume) |
| `/126mail classify` | Scan and classify all emails by sender domain |
| `/126mail cleanup` | Interactively bulk-delete ads/subscriptions |
| `/126mail strip` | Download large attachments locally, then replace originals with lightweight stubs on server |
| `/126mail status` | Show current mailbox stats and cleanup progress |

## Setup — Step by Step

### Step 1: Enable IMAP Access on 126.com

1. Log in to https://mail.126.com in a browser
2. Go to **Settings (设置)** > **POP3/SMTP/IMAP**
3. Enable **IMAP/SMTP Service**
4. Generate an **Authorization Code** (授权码) — this is NOT your login password
5. Save this code securely

### Step 2: Configure the Skill

Provide your credentials when prompted:

```
MAIL126_ADDRESS=your_email@126.com
MAIL126_AUTH_CODE=your_authorization_code
```

### Step 3: Verify Connection

Run `/126mail setup` to test the IMAP connection. The skill will:
- Connect to `imap.126.com:993` (SSL)
- Send the required ID command (126 rejects clients without it)
- List all folders with email counts and total sizes

## IMAP API Reference

126.com IMAP has several quirks. This skill handles them automatically, but here is the reference for transparency:

### Connection Requirements

| Item | Value |
|------|-------|
| Server | `imap.126.com` |
| Port | `993` (SSL) |
| Auth | LOGIN with authorization code (not password) |
| **ID Command** | **REQUIRED** — must send `ID ("name" "IMAPClient" "version" "1.0.0" ...)` after login, or server rejects operations |

### Folder Name Encoding (Modified UTF-7)

Chinese folder names are encoded. Common mappings:

| Display Name | IMAP Name |
|-------------|-----------|
| 已发送 (Sent) | `&XfJT0ZAB-` |
| 草稿箱 (Drafts) | `&g0l6P3ux-` |
| 已删除 (Trash) | `&XfJSIJZk-` |
| 垃圾邮件 (Spam) | `&V4NXPpCuTvY-` |

### Rate Limits

| Operation | Limit |
|-----------|-------|
| FETCH (download) | ~4GB per session before throttling |
| SEARCH, SIZE queries | Unlimited |
| UID SEARCH ALL | ~3 seconds |
| UID SEARCH FROM | ~35 seconds per query |
| UID COPY | ~0.25 sec/email, optimal batch = 50 |

### Critical Rule: Always Use UID, Never Sequence Numbers

**This is the most important lesson.** IMAP sequence numbers shift after any deletion. If you delete email #5, then email #6 becomes #5, #7 becomes #6, etc. Using sequence numbers after deletions WILL operate on wrong emails. Always use `UID FETCH`, `UID STORE`, `UID COPY`, `UID SEARCH`.

## Phase 1: Local Backup (`/126mail backup`)

### What It Does
- Downloads all emails (including attachments) from all folders
- Saves each email as `message.eml` with a `_meta.json` sidecar
- Organized as: `backup_dir/folder_name/UID_subject/`
- Supports **resume on interruption** — tracks progress in `_download_progress.json`

### Batch Strategy
- Downloads in batches of **500 emails or 4GB** (whichever comes first)
- Pauses between batches to avoid hitting 126's rate limit
- Reconnects every 20 emails to prevent timeout
- Socket timeout set to 300 seconds for large attachments

### Key Decisions for User

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Which folders to back up | All / INBOX only / Custom | Start with INBOX + Sent |
| Include attachments | Yes / Skip large ones | Yes (they're your data) |
| Batch size | 100-500 emails | 500 (maximize before rate limit) |

## Phase 2: Email Classification (`/126mail classify`)

### What It Does
1. Fetches metadata (subject, from, to, date, size) for ALL emails via IMAP — no content download needed
2. Groups emails by sender domain
3. Classifies into categories:
   - **Platform/Ads**: LinkedIn, Amazon, PayPal, JD, Taobao, etc.
   - **Financial Notifications**: Banks, brokers, payment services
   - **Services**: Cloud, SaaS, travel booking
   - **Personal**: Individual senders, known contacts
4. Outputs `all_emails_meta.json` (full index) and `email_classification.json`

### Metadata-First Approach
- SEARCH and ENVELOPE operations are NOT rate-limited on 126
- Can index 40,000+ emails in minutes
- UID is tagged on every record for later operations

### Key Decisions for User

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Classification strictness | Aggressive / Conservative | Conservative — review before delete |
| Time cutoff for deletion | All time / Before 2025 / Custom | Before current year (keep recent) |
| Domain whitelist | Auto / Manual review | Always manually review KEEP list |

## Phase 3: Bulk Cleanup (`/126mail cleanup`)

### What It Does
1. Shows classified email counts by category
2. User reviews and approves DELETE_DOMAINS list and KEEP_DOMAINS list
3. **Safety net**: Copies target emails to a staging folder (e.g., "广告邮件") BEFORE deleting from INBOX
4. Deletes from INBOX via `UID STORE +FLAGS \Deleted` + `EXPUNGE`
5. Random-sample verification (10 emails spot-checked)

### The Safe Deletion Flow

```
INBOX emails  ──UID COPY──>  广告邮件夹 (staging copy)
     │
     └── UID STORE \Deleted + EXPUNGE (remove from INBOX)

User verifies in web client...

广告邮件夹  ──permanent delete──>  Gone (only after user confirms)
```

### Key Decisions for User

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Deletion scope | By domain / By category / By date | By domain — most precise |
| Staging folder | Create new / Use existing | Create "广告邮件" for review |
| When to purge staging | Immediately / After 7 days / Manual | Manual — check in web client first |
| Verification sample size | 5 / 10 / 20 | 10 random emails |

### Common DELETE_DOMAINS Reference

```
linkedin.com, crunchbase.com, amazon.com, jd.com, 
service.taobao.com, airbnb.com, booking.com, uber.com,
ctrip.com, trip.com, godaddy.com, coursera.org,
service.netease.com, insideapple.apple.com,
accounts.google.com, intl.paypal.com, citibank.com,
mail.meituan.com, sf-express.com, ...
```

### Common KEEP_DOMAINS Reference

```
svb.com, gusto.com, berkeley.edu, alibaba-inc.com,
live.com, 139.com, pku.edu.cn, ...
```

Always let the user review and customize these lists based on their own email history.

## Phase 4: Large Attachment Stripping (`/126mail strip`)

### What It Does (Two-Phase Safety Process)

**Phase A — Download Only (read-only, no server changes)**
1. Search all folders for emails > threshold (default 50MB)
2. Download each email's attachments to local backup
3. Save metadata (`_meta.json`) for each
4. Track progress in `_progress.json`
5. Reconnect every 5 emails to avoid timeout

**Phase B — Strip and Replace (destructive, requires explicit confirmation)**
1. For each downloaded email:
   - Fetch the full message with FLAGS and INTERNALDATE
   - Remove attachment parts from the MIME structure
   - Append a notice: `[附件已移除 - 已备份到本地]` with file list and original size
   - Upload the lightweight replacement (preserving original flags and date)
   - Delete the original heavy email
2. Track progress — resumable if interrupted

### Storage Savings Example

| Before | After | Saved |
|--------|-------|-------|
| 70 emails @ 50-200MB each | 70 emails @ 5-50KB each | ~3.4GB |

### Key Decisions for User

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Size threshold | 10MB / 20MB / 50MB / 100MB | 50MB (best ROI) |
| Which folders | All / INBOX only | All folders |
| Verify downloads before stripping | Yes / Skip | Always Yes — Phase B is destructive |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `LOGIN failed` | Wrong auth code or IMAP not enabled | Re-generate authorization code at 126 settings |
| `ID command rejected` | Missing ID command after login | Skill sends ID automatically — report if this occurs |
| `FETCH timeout` | Rate limit hit (~4GB) | Save progress, wait 1-2 hours, resume |
| `BAD command` | Folder name encoding wrong | Skill uses correct Modified UTF-7 |
| Sequence number mismatch | Used sequence instead of UID | Skill always uses UID operations |

## Progress Tracking

All operations save progress to JSON files:
- `_download_progress.json` — Full backup progress
- `_progress.json` — Large email strip progress
- `cleanup_progress.md` — Human-readable summary

This means every operation is **resumable**. If your connection drops, rate limit hits, or you close your laptop — just run the command again and it picks up where it left off.

## Recommended Workflow

1. `/126mail setup` — Connect and verify
2. `/126mail status` — See current mailbox state
3. `/126mail backup` — Full local backup (run multiple times if rate-limited)
4. `/126mail classify` — Index and classify all emails
5. `/126mail cleanup` — Review and bulk-delete ads/subscriptions
6. `/126mail strip` — Reclaim space from large attachments
7. `/126mail status` — Verify results

## Technical Notes

- Python 3.6+ with `imaplib` and `email` (standard library only, no pip dependencies)
- All IMAP operations use SSL (port 993)
- Modified UTF-7 encoding handled automatically for Chinese folder names
- ID command sent on every connection to satisfy 126's requirement
- All file names sanitized to remove illegal characters
- Duplicate attachment filenames handled with suffix numbering
