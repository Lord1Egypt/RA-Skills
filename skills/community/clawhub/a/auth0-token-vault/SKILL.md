---
name: auth0-token-vault
description: >
  Access third-party services (Gmail, Slack, Google Calendar, GitHub) and custom
  Auth0 connections on behalf of authenticated users via Auth0 Token Vault. Use
  when the user wants to search, read, send, or manage emails, manage calendar
  events, interact with Slack, manage GitHub repos/issues/PRs/notifications, make
  authenticated API calls to third-party services or custom identity providers,
  connect or disconnect external services, or check their authentication and
  connection status. Wraps the auth0-tv CLI.
compatibility: Requires Node.js 20+ and auth0-tv installed globally (npm i -g auth0-token-vault-cli)
license: MIT
allowed-tools: Bash(auth0-tv *)
metadata:
  author: deepu105
  version: '0.3'
  openclaw:
    emoji: "\U0001F510"
    requires:
      bins:
        - auth0-tv
    os:
      - darwin
      - linux
    install:
      - id: npm
        kind: node
        package: 'auth0-token-vault-cli'
        bins: [auth0-tv]
        label: 'Install auth0-tv (npm)'
---

# Auth0 Token Vault CLI

Use the `auth0-tv` command-line tool to access third-party services on behalf of
authenticated users via Auth0 Token Vault.

## Current status

- Auth status: !`auth0-tv --json status 2>/dev/null || echo '{"error":{"code":"not_configured","message":"auth0-tv not configured or not logged in"}}'`

## First-time setup

If `auth0-tv --json status` returns a `not_configured` error, guide the user through setup:

1. **Run the interactive setup wizard** (recommended — handles all steps automatically):

   ```bash
   auth0-tv init
   ```

   The `init` wizard will check prerequisites, configure Token Vault, set up callback URLs, retrieve credentials, and authenticate — all in one guided flow.

   All setup steps require human interaction. Do not attempt to run them autonomously.

### Manual setup (alternative)

If the wizard is not suitable, guide the user through manual setup:

1. **Install Auth0 CLI** (if not already installed):

   ```bash
   brew tap auth0/auth0-cli && brew install auth0
   ```

2. **Run the Token Vault setup wizard** (interactive — requires human):

   ```bash
   npx configure-auth0-token-vault
   ```

   The wizard handles Auth0 CLI login automatically. When prompted:
   - Select **Create a new application** (or use an existing one)
   - Select **Regular Web Application** for the app type
   - Select **Refresh Token Exchange** for the Token Vault configuration

   Note the **Client ID** from the output.

3. **Configure callback URLs** using the Auth0 CLI (replace `<APP_ID>` with the Client ID):

   ```bash
   auth0 apps update <APP_ID> \
     --callbacks "http://127.0.0.1:18484/callback,http://127.0.0.1:18485/callback,http://127.0.0.1:18486/callback,http://127.0.0.1:18487/callback,http://127.0.0.1:18488/callback,http://127.0.0.1:18489/callback" \
     --logout-urls "http://127.0.0.1:18484,http://127.0.0.1:18485,http://127.0.0.1:18486,http://127.0.0.1:18487,http://127.0.0.1:18488,http://127.0.0.1:18489"
   ```

4. **Get the client secret** (needed during `auth0-tv login`):

   ```bash
   auth0 apps show <APP_ID> --reveal-secrets
   ```

5. **Log in with auth0-tv:**
   ```bash
   auth0-tv login
   ```

All setup steps require human interaction. Do not attempt to run them autonomously.

## When to use this skill

- The user asks to read, search, send, reply, forward, archive, or delete emails
- The user wants to manage email drafts or labels
- The user wants to view, create, update, or delete Google calendar events
- The user wants to search Slack messages, post to channels, or manage their Slack status
- The user wants to list repos, view issues/PRs, create issues, search code, or manage GitHub notifications
- The user wants to make an authenticated API call to a third-party service
- The user wants to connect or disconnect a third-party service (Gmail, Google Calendar, Slack, GitHub)
- The user wants to connect a custom Auth0 connection (any social/enterprise identity provider configured on their tenant)
- The user asks about their authentication or connection status

## Key patterns

### Always use --json mode

All commands must use `--json` for structured output:

```bash
auth0-tv --json <command>
```

Alternatively, set `AUTH0_TV_OUTPUT=json` in the environment to avoid passing `--json` on every call.

### Destructive actions require --confirm

Commands that modify data (send, delete, archive, forward, reply, draft send, draft delete) require `--confirm`:

```bash
auth0-tv --json --confirm gmail send --to user@example.com --subject "Subject" --body "Body"
```

### Exit codes and recovery

| Code | Meaning             | Recovery action                                   |
| ---- | ------------------- | ------------------------------------------------- |
| 0    | Success             | Parse JSON output                                 |
| 1    | General error       | Report error to user                              |
| 2    | Invalid input       | Check command syntax and required flags           |
| 3    | Auth required       | Tell the user to run `auth0-tv login`             |
| 4    | Connection required | Tell the user to run `auth0-tv connect <service>` |
| 5    | Service error       | Retry or report upstream API failure              |
| 6    | Network error       | Check connectivity, retry                         |

**Important:** Exit codes 3 and 4 require human intervention — `login` and `connect` open a browser for OAuth. Do not attempt to run these commands autonomously; instead, tell the user what to run.

Auth and connect/logout callback servers default to trying ports `18484-18489`. If that range is blocked, pass the global `--port <number>` flag or set `AUTH0_TV_PORT` to force a specific port (that port must be allowed in Auth0 app callback settings).

### Body input for email composition

For `send`, `reply`, and `draft create`, the message body can be provided via:

- `--body "inline text"` — short messages
- `--body-file ./message.txt` — longer messages from a file
- stdin: `echo "body" | auth0-tv --json --confirm gmail send --to ... --subject ...`

Prefer `--body-file` or stdin for messages containing special characters.

## Available commands

### Authentication & setup

- `auth0-tv login [--reconfigure]` — authenticate via browser (human-in-the-loop)
- `auth0-tv logout` — clear stored credentials
- `auth0-tv status` — show current user and connected services
- `auth0-tv connect <service>` — connect a known service via browser (human-in-the-loop)
- `auth0-tv connect <connection-name> --scopes <scopes> --allowed-domains <domains>` — connect any Auth0 connection by name
- `auth0-tv disconnect <service>` — disconnect a service or custom connection (local token only by default)
- `auth0-tv disconnect <service> --remote` — disconnect a service and remove the server-side connection
- `auth0-tv connections` — list connected services (remote accounts with local token status)

### Gmail

- `auth0-tv gmail search <query>` — search messages (supports Gmail search syntax)
- `auth0-tv gmail read <messageId>` — read a message
- `auth0-tv gmail send` — send a new message (destructive)
- `auth0-tv gmail reply <messageId>` — reply to a message (destructive)
- `auth0-tv gmail forward <messageId>` — forward a message (destructive)
- `auth0-tv gmail archive <messageId>` — archive a message (destructive)
- `auth0-tv gmail delete <messageId>` — move to trash (destructive)
- `auth0-tv gmail labels` — list labels
- `auth0-tv gmail label <messageId>` — add/remove labels
- `auth0-tv gmail draft create` — create a draft
- `auth0-tv gmail draft list` — list drafts
- `auth0-tv gmail draft send <draftId>` — send a draft (destructive)
- `auth0-tv gmail draft delete <draftId>` — delete a draft (destructive)

### Google Calendar

- `auth0-tv calendar list` — list calendars
- `auth0-tv calendar events [calendarId]` — list events (default: primary calendar)
- `auth0-tv calendar get <eventId>` — get event details
- `auth0-tv calendar create` — create an event (destructive)
- `auth0-tv calendar update <eventId>` — update an event (destructive)
- `auth0-tv calendar delete <eventId>` — delete an event (destructive)
- `auth0-tv calendar quick-add <text>` — create event from natural language (destructive)

### Slack

- `auth0-tv slack channels` — list channels
- `auth0-tv slack messages <channel>` — list messages in a channel
- `auth0-tv slack search <query>` — search messages (Slack search syntax)
- `auth0-tv slack post <channel>` — post a message (destructive)
- `auth0-tv slack reply <channel> <threadTs>` — reply to a thread (destructive)
- `auth0-tv slack react <channel> <timestamp>` — add/remove emoji reaction
- `auth0-tv slack users` — list users
- `auth0-tv slack user <userId>` — get user info
- `auth0-tv slack status` — set your status

### GitHub

- `auth0-tv github repos` — list your repositories
- `auth0-tv github repo <owner/repo>` — get repository details
- `auth0-tv github issues <owner/repo>` — list issues
- `auth0-tv github issue get <owner/repo> <number>` — get issue details
- `auth0-tv github issue create <owner/repo>` — create an issue (destructive)
- `auth0-tv github issue comment <owner/repo> <number>` — comment on an issue (destructive)
- `auth0-tv github issue close <owner/repo> <number>` — close an issue (destructive)
- `auth0-tv github prs <owner/repo>` — list pull requests
- `auth0-tv github pr get <owner/repo> <number>` — get PR details
- `auth0-tv github pr comment <owner/repo> <number>` — comment on a PR (destructive)
- `auth0-tv github notifications` — list notifications
- `auth0-tv github notification read <id>` — mark notification as read (destructive)
- `auth0-tv github search repos <query>` — search repositories
- `auth0-tv github search code <query>` — search code
- `auth0-tv github search issues <query>` — search issues and PRs

### API passthrough (fetch)

- `auth0-tv fetch <service> <url>` — make an authenticated HTTP request to an allowed domain
- `auth0-tv fetch <connection-name> <url>` — fetch using a custom Auth0 connection token
- `auth0-tv fetch <service> <url> -X POST -d '{"key":"value"}'` — POST with inline body
- `auth0-tv fetch <service> <url> -X POST --data-file ./body.json` — POST with body from file
- `auth0-tv fetch <service> <url> -H "Accept: text/plain"` — add custom headers

Known services have default allowed domains built in. Custom connections require `--allowed-domains` to be set during `connect`:

| Service    | Default allowed domains    |
| ---------- | -------------------------- |
| `gmail`    | `*.googleapis.com`         |
| `calendar` | `*.googleapis.com`         |
| `github`   | `api.github.com`           |
| `slack`    | `slack.com`, `*.slack.com` |

Additional domains can be added via `--allowed-domains` on `connect`. Custom connections have no default domains — you must specify `--allowed-domains` when connecting. Only HTTPS URLs are allowed.

See [references/commands.md](references/commands.md) for full command reference with flags and JSON output examples.
