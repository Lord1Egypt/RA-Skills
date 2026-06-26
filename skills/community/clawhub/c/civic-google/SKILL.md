---
name: civic-google
description: Use gog (Google CLI) without manual OAuth setup — Civic handles token management automatically
metadata: {"openclaw": {"requires": {"bins": ["gog"], "env": ["CIVIC_TOKEN"]}, "emoji": "🔑"}}
---

This skill describes the `@civic/openclaw-google` plugin, which lets agents use `gog` (the Google Workspace CLI) without the user having to create a Google Cloud project, configure OAuth credentials, or manage tokens. Civic acts as an OAuth proxy — it provides the OAuth client, stores tokens encrypted server-side, refreshes them automatically, and the plugin requests only the scope each command actually needs.

## Privacy and security

- **What is sent to Civic:** The plugin sends the `gog` command prefix (e.g. `gog gmail send`) over HTTPS to `app.civic.com` for scope resolution. The proxy reads only the command prefix to determine which OAuth scope is needed — command arguments (email addresses, search queries, file names) are not logged, stored, or used by the proxy.
- **CIVIC_TOKEN:** This is the user's own API key from their Civic account at app.civic.com. It authenticates the user to their own account and is never shared. It is sent as a Bearer token over HTTPS.
- **Token handling:** OAuth access tokens are short-lived (~1 hour), stored encrypted (AES-256) on Civic's servers, and refreshed automatically. The agent never sees OAuth client secrets or refresh tokens.
- **Source code:** The plugin is open source at https://github.com/civicteam/openclaw-google and published on npm as `@civic/openclaw-google`.

## Setup

1. Install the plugin:
   ```bash
   openclaw plugins install @civic/openclaw-google
   ```

2. Install gog (the Google CLI):
   ```bash
   brew install gog
   ```

3. Set your Civic API token in the gateway environment:
   ```bash
   CIVIC_TOKEN=<your-token-from-app.civic.com>
   ```
   Get your token from app.civic.com -> Settings -> API Keys.

4. Restart the gateway.

## How it works

1. Agent calls `gog gmail search newer_than:1d`
2. Plugin intercepts the `exec` tool call via a `before_tool_call` hook
3. Plugin sends the command prefix to the Civic proxy for scope resolution
4. Proxy matches `gog gmail` -> `gmail.readonly` scope
5. If authorized: returns a short-lived access token, plugin sets `GOG_ACCESS_TOKEN` env var, `gog` runs
6. If not yet authorized: blocks the tool call and surfaces an auth URL for the user to consent
7. After first consent per scope, all future calls work automatically

## Supported services and scope mapping

The plugin maps each `gog` subcommand to the narrowest OAuth scope required. Write operations get specific scopes; unrecognized subcommands fall back to read-only.

### Gmail
- `gog gmail send` — gmail.send
- `gog gmail draft`, `gog gmail drafts` — gmail.compose
- `gog gmail trash`, `archive`, `read`, `unread`, `batch` — gmail.modify
- `gog gmail` (catch-all) — gmail.readonly

### Calendar
- `gog calendar create`, `update`, `delete`, `respond`, `subscribe` — calendar.events
- `gog calendar` (catch-all) — calendar.readonly

### Drive
- `gog drive upload`, `create`, `update`, `delete`, `move`, `rename`, `share`, `copy`, `import` — drive.file
- `gog drive transfer` — drive (full access, required for ownership transfer)
- `gog drive` (catch-all) — drive.readonly

### Docs
- `gog docs create`, `edit`, `append` — documents
- `gog docs copy`, `delete`, `import` — documents + drive.file
- `gog docs export` — documents.readonly + drive.file
- `gog docs` (catch-all) — documents.readonly + drive.readonly

### Sheets
- `gog sheets write`, `append`, `delete`, `insert`, `format`, `merge`, `freeze`, `resize` — spreadsheets
- `gog sheets create` — spreadsheets + drive.file
- `gog sheets` (catch-all) — spreadsheets.readonly + drive.readonly

### Slides
- `gog slides create`, `copy` — presentations + drive.file
- `gog slides edit`, `update`, `duplicate`, `delete` — presentations
- `gog slides` (catch-all) — presentations.readonly + drive.readonly

### Tasks
- `gog tasks add`, `done`, `delete`, `move`, `update` — tasks
- `gog tasks` (catch-all) — tasks.readonly

### Contacts
- `gog contacts create`, `update`, `delete`, `merge`, `batch` — contacts
- `gog contacts` (catch-all) — contacts.readonly

### Chat
- `gog chat send` — chat.messages.create
- `gog chat create` — chat.spaces
- `gog chat delete` — chat.messages
- `gog chat` (catch-all) — chat.spaces.readonly + chat.messages.readonly

### Forms
- `gog forms create`, `update`, `delete` — forms.body
- `gog forms` (catch-all) — forms.body.readonly + forms.responses.readonly

### Apps Script
- `gog appscript run` — script.projects
- `gog appscript deploy` — script.deployments
- `gog appscript` (catch-all) — script.projects.readonly + drive.readonly

## Troubleshooting

- **"No CIVIC_TOKEN configured"** — Set `CIVIC_TOKEN` in your gateway environment. Get it from app.civic.com -> Settings -> API Keys.
- **Auth URL keeps appearing** — The user needs to click the authorization link and complete the Google consent screen. Each scope requires separate consent.
- **Token errors after working previously** — The user may have revoked access in their Google account settings. Re-authorize by triggering any `gog` command.

## Custom proxy URL

For local development, set `OPENCLAW_PROXY_URL` in the gateway environment:
```bash
OPENCLAW_PROXY_URL=http://localhost:3013/openclaw
```
