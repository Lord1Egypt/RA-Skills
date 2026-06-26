---
name: docker-mailbox
description: Multi-mailbox IMAP/SMTP control plane exposed as a REST API + MCP server (streamable HTTP) on a single port. Read, search, send, mark-seen, and delete mail across multiple inboxes in one call — `GET /inbox` fans out across every IMAP account in parallel and returns a merged, newest-first feed. Use when you need an agent (or a script, or a curl one-liner) to drive one or more real mail accounts without standing up a webmail UI, a message store, or any per-provider client library. Stdlib `imaplib`/`smtplib` under the hood, FastAPI on top, bearer-token auth optional.
compatibility: Requires curl and a running mailboxd instance. MAILBOX_URL env var must be set. MAILBOX_TOKEN is optional — only needed if the server was started with `auth.tokens` configured.
metadata:
  author: psyb0t
  homepage: https://github.com/psyb0t/docker-mailbox
---

# docker-mailbox

REST + MCP shim over IMAP/SMTP. Point it at one or more mail accounts via a YAML config, get back **one HTTP API + one MCP server on the same port** (MCP rides a streamable-HTTP endpoint at `/mcp`). No webmail. No DB. No message store. Stateless — restart it and nothing's lost because nothing was ever kept.

The killer endpoint is `GET /inbox` — it hits every IMAP account in parallel, runs the same structured search on each, merges newest-first, and tags every result with which mailbox it came from. "Show me everything from `boss@corp.com`," "what's unread right now," "what came in this morning" — one call, no fanout dance on the client side.

For installation and setup, see [references/setup.md](references/setup.md).

## Setup

The API should already be running. Set the base URL and (if configured) the bearer token:

```bash
export MAILBOX_URL=http://localhost:8000
export MAILBOX_TOKEN=your_token_here   # omit if auth.tokens is empty in config
```

**Verify:**

```bash
curl -s $MAILBOX_URL/health
# {"ok": true, "version": "0.1.0"}

curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" $MAILBOX_URL/mailboxes | jq
```

`/health` is **always open** — point liveness probes at it without worrying about auth.

Auth is optional. If `auth.tokens` is empty/missing in the server config, all endpoints are open. If it's set, every non-`/health` request needs `Authorization: Bearer <one of auth.tokens>` and returns `401` (with `WWW-Authenticate: Bearer`) on miss. Tokens are constant-time compared. The same gate covers `/mcp`.

## How It Works

`GET` to read, `POST` to send/mark/create, `DELETE` to delete. All bodies are JSON. All responses are JSON.

Every error response:

```json
{"detail": "description of what went wrong"}
```

Status codes:

| Status | When                                                                                       |
| ------ | ------------------------------------------------------------------------------------------ |
| `401`  | Missing or invalid bearer (when auth is on).                                                |
| `404`  | Unknown mailbox name in the URL.                                                            |
| `409`  | Mailbox doesn't have the requested protocol (IMAP endpoint on an SMTP-only mailbox).        |
| `422`  | Request body validation failed (pydantic).                                                  |
| `502`  | The IMAP / SMTP server upstream rejected the operation.                                     |

UIDs (not sequence numbers) are used for every message identifier so IDs stay stable across server-side mutations.

## API Reference

### Health

```bash
curl -s $MAILBOX_URL/health
# {"ok": true, "version": "0.1.0"}
```

### Mailboxes

```bash
curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" $MAILBOX_URL/mailboxes
```

```json
{
  "mailboxes": [
    { "name": "personal", "description": "Gmail", "imap": true, "smtp": true },
    { "name": "work",     "description": "",       "imap": true, "smtp": true }
  ]
}
```

`name` is the URL-safe handle (matches `[a-zA-Z0-9_-]+`, unique) used in every other path. The `imap` / `smtp` booleans tell you which protocols the server has configured for that mailbox — if `imap: false`, you can't list/fetch/delete; if `smtp: false`, you can't send.

### Unified inbox (the main read endpoint)

`GET /inbox` fans out across **every IMAP-configured mailbox** in parallel, runs the same structured search against each one, merges newest-first, and tags each message with which account it came from. Per-mailbox failures land in `errors` instead of aborting the whole call.

| Query param                                      | What it does                                                                                                                              |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `mailbox`                                        | CSV filter by mailbox name (`personal`) **or** email address (`me@gmail.com`). Omit to search all IMAP mailboxes.                          |
| `from`, `to`, `subject`, `body`, `text`          | IMAP SEARCH predicates. `text` is full-text across headers + body.                                                                         |
| `since`, `before`                                | IMAP date filters, e.g. `1-Jan-2026`.                                                                                                      |
| `unseen`, `seen`, `flagged`, `answered`          | Boolean flag filters.                                                                                                                      |
| `larger_than`, `smaller_than`                    | Size filters in bytes.                                                                                                                     |
| `folder`                                         | IMAP folder name (default `INBOX`).                                                                                                        |
| `limit`                                          | Max merged results, ≤ 500 (default 50).                                                                                                    |

```bash
# everything from one sender, all accounts
curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" \
  "$MAILBOX_URL/inbox?from=boss@corp.com&limit=20" | jq

# unread mail in just two accounts
curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" \
  "$MAILBOX_URL/inbox?mailbox=personal,work&unseen=true" | jq

# everything since yesterday, full-text "invoice"
curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" \
  "$MAILBOX_URL/inbox?since=$(date -d 'yesterday' +%-d-%b-%Y)&text=invoice" | jq

# search a specific folder (e.g. Spam)
curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" \
  "$MAILBOX_URL/inbox?folder=Spam&limit=10" | jq
```

Response:

```json
{
  "messages": [
    {
      "uid": "1234",
      "mailbox": "personal",
      "mailbox_address": "me@gmail.com",
      "from": "boss@corp.com",
      "to": "me@gmail.com",
      "subject": "weekly sync",
      "date": "Mon, 18 May 2026 09:15:00 +0000",
      "message_id": "<...@corp.com>",
      "flags": ["\\Seen"]
    }
  ],
  "errors": [
    { "mailbox": "work", "error": "login failed: ..." }
  ]
}
```

### Per-mailbox IMAP

When you want to target one account directly:

```bash
# Folders
curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" \
  $MAILBOX_URL/mailboxes/personal/folders

# List newest-first headers — raw IMAP SEARCH criteria
curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" \
  "$MAILBOX_URL/mailboxes/personal/messages?folder=INBOX&limit=20&search=UNSEEN"

# Structured single-mailbox search — same query params as /inbox minus `mailbox`
curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" \
  "$MAILBOX_URL/mailboxes/personal/search?from=boss@corp.com&since=1-May-2026"

# Fetch one full message (decoded body_text + body_html + attachment metadata)
curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" \
  "$MAILBOX_URL/mailboxes/personal/messages/1234?folder=INBOX"

# Same but also get `body_reader` — HTML stripped to clean text/markdown
# (perfect for feeding into an LLM without all the table/style chrome)
curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" \
  "$MAILBOX_URL/mailboxes/personal/messages/1234?folder=INBOX&reader=true"

# Mark seen / unseen
curl -s -X POST -H "Authorization: Bearer $MAILBOX_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"seen": true}' \
  "$MAILBOX_URL/mailboxes/personal/messages/1234/seen?folder=INBOX"

# Delete (flag \Deleted + EXPUNGE — gone, really gone)
curl -s -X DELETE -H "Authorization: Bearer $MAILBOX_TOKEN" \
  "$MAILBOX_URL/mailboxes/personal/messages/1234?folder=INBOX"
```

`/messages` `search` is **raw IMAP SEARCH** (e.g. `ALL`, `UNSEEN`, `FROM foo@bar`, `(UNSEEN FROM foo@bar)`). `/search` is the structured query DSL — same params as `/inbox` minus `mailbox`. Use whichever's easier.

Full-message fetch returns:

```json
{
  "uid": "1234",
  "from": "boss@corp.com",
  "to": "me@gmail.com",
  "cc": "",
  "subject": "weekly sync",
  "date": "Mon, 18 May 2026 09:15:00 +0000",
  "message_id": "<...@corp.com>",
  "body_text": "plain text body",
  "body_html": "<p>html body</p>",
  "body_reader": null,
  "attachments": [
    {"filename": "agenda.pdf", "content_type": "application/pdf", "size": 12345}
  ]
}
```

`body_reader` is `null` unless you pass `reader=true`. When enabled it falls back to `body_text` if no HTML body exists, otherwise it's the HTML body stripped to readable markdown (links inline, images dropped, tables flattened, no styles/scripts).

#### How reader mode works

Runs the HTML body through [html2text](https://github.com/Alir3z4/html2text) configured for LLM consumption: `body_width=0` (no wrap), `ignore_images=True` (kills `<img>` tracking pixels), `unicode_snob=True` (real unicode, no smart-quote mangling). `<style>`, `<script>`, `<head>`, comments and all inline-style chrome get dropped. Headings → `#`, bold/italic preserved, `<a href="x">text</a>` → `[text](x)` inline, lists/tables converted to markdown equivalents.

The original `body_text` and `body_html` are still returned — `body_reader` is additive. UI clients can render HTML, agents can read markdown, attachments stay as metadata.

Useful when the `text/plain` part is missing or an auto-generated "view in HTML client" stub (which is true for most marketing/transactional mail). Limitations: reply-quote chains aren't stripped, table-layout emails come through as pipe-tables (faithful but visually noisy).

### SMTP

```bash
curl -s -X POST -H "Authorization: Bearer $MAILBOX_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "to":           ["dest@example.com"],
    "cc":           ["copy@example.com"],
    "bcc":          ["hidden@example.com"],
    "subject":      "hi",
    "body_text":    "plain text body",
    "body_html":    "<p>optional html body</p>",
    "from_address": "Me <me@example.com>",
    "reply_to":     "noreply@example.com"
  }' \
  $MAILBOX_URL/mailboxes/personal/send
```

Required: `to` (non-empty), `subject`, and at least one of `body_text` / `body_html`. Both bodies = `multipart/alternative`.

The SMTP client automatically sets `Date`, a domain-aligned `Message-ID`, and a Thunderbird-shaped `User-Agent` — provider spam filters get hostile when those are missing or sloppy, so we play the game. Response:

```json
{
  "from":       "Me <me@example.com>",
  "to":         "dest@example.com",
  "subject":    "hi",
  "message_id": "<177906914784.1.7220590975517922818@example.com>"
}
```

## MCP server

Same operations exposed as MCP tools over **streamable HTTP** at `POST /mcp` (same port, same bearer). One flat tool set — every per-mailbox op takes `mailbox` as a parameter (the configured name OR the email address), so the catalog stays constant-sized no matter how many accounts you configure:

```
mailboxes                   # discovery: list configured mailboxes + capabilities
inbox                       # unified read across all IMAP mailboxes (mailbox= filter)
list_folders                # (mailbox)
list_messages               # (mailbox, folder, limit, search)
search                      # (mailbox, from, subject, since, ...)
get_message                 # (mailbox, uid, reader=true → +body_reader)
delete_message              # (mailbox, uid)
mark_seen                   # (mailbox, uid, seen)
send                        # (mailbox, to, subject, body_text/html, ...)
```

Discovery flow for an agent: call `mailboxes` to see what's available, then pass the chosen name (`"personal"`) or address (`"me@gmail.com"`) as the `mailbox` argument. For cross-account reads use `inbox` — `inbox(from="boss@corp.com")` fans out across every IMAP-enabled mailbox in one call. IMAP-only tools only appear if at least one mailbox has IMAP; same for SMTP. No dead buttons.

There is **no stdio transport**. Point MCP clients at `$MAILBOX_URL/mcp`. The endpoint speaks the full streamable-HTTP protocol (`GET` opens SSE, `POST` sends requests, `DELETE` terminates the session). `.mcp.json` snippet:

```json
{
  "mcpServers": {
    "mailbox": {
      "transport": "streamable-http",
      "url": "http://localhost:8000/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_HERE"
      }
    }
  }
}
```

Drop the `headers` block if you're running without `auth.tokens`.

## Common Workflows

### Find and delete

```bash
# 1. Find UIDs matching the criteria
HITS=$(curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" \
  "$MAILBOX_URL/inbox?from=newsletter@spam.io&limit=500" | jq -r '.messages[] | "\(.mailbox) \(.uid)"')

# 2. Delete each (per-mailbox endpoint since DELETE is single-mailbox)
echo "$HITS" | while read -r mailbox uid; do
  curl -s -X DELETE -H "Authorization: Bearer $MAILBOX_TOKEN" \
    "$MAILBOX_URL/mailboxes/$mailbox/messages/$uid"
done
```

### Send-to-self e2e sanity check

```bash
MARKER="e2e-$(uuidgen | cut -c1-8)"

# 1. Send marker to self
curl -s -X POST -H "Authorization: Bearer $MAILBOX_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"to\": [\"me@gmail.com\"], \"subject\": \"ping $MARKER\", \"body_text\": \"$MARKER\"}" \
  "$MAILBOX_URL/mailboxes/personal/send"

# 2. Search for it (may take a few seconds to land)
for i in 1 2 3 4 5; do
  sleep 2
  FOUND=$(curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" \
    "$MAILBOX_URL/inbox?subject=$MARKER" | jq -r '.messages | length')
  [ "$FOUND" -gt 0 ] && break
done
```

### Pull unread across everything, format for a digest

```bash
curl -s -H "Authorization: Bearer $MAILBOX_TOKEN" \
  "$MAILBOX_URL/inbox?unseen=true&limit=100" \
  | jq -r '.messages[] | "\(.mailbox)\t\(.from)\t\(.subject)"' \
  | column -t -s $'\t'
```

## Tips

- Date filters (`since`, `before`) use **IMAP date format** (`1-Jan-2026`), not ISO — `date -d ... +%-d-%b-%Y` is your friend.
- `larger_than` / `smaller_than` are in **bytes**.
- `folder` defaults to the mailbox's `default_folder` (usually `INBOX`). Provider-specific folder names: Gmail = `[Gmail]/Spam`, GMX/Yahoo = `Spam`, Outlook = `Junk Email`. Use `GET /mailboxes/<name>/folders` to discover.
- A self-send may land in Spam on some providers (GMX especially) due to provider-side self-send heuristics even with proper headers — search `folder=Spam` if you don't see it in INBOX.
- Gmail / Yahoo / etc. need **app passwords**, not your account password. Generate one in the provider's security settings.
- `delete` is a real EXPUNGE — there is no trash bin equivalent unless the server moves to a Trash folder first. If you want soft delete, MOVE first then delete; mailboxd doesn't expose move yet.
- Per-mailbox blowups in `/inbox` come back in the `errors` array — always check it, one dead account shouldn't blind you to the rest.
- Bearer tokens live in the server's `config.yaml` under `auth.tokens` — list with multiple tokens to rotate without downtime.
