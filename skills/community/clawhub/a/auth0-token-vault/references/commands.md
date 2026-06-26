# auth0-tv Command Reference

Full command reference for agent invocation. All examples use `--json` mode.

## Global options

| Flag                  | Description                                                          |
| --------------------- | -------------------------------------------------------------------- |
| `--json`              | Output structured JSON (required for agent use)                      |
| `--confirm` / `--yes` | Skip destructive-action confirmation prompts                         |
| `--browser <app>`     | Browser for auth flows (e.g. `firefox`, `google-chrome`)             |
| `--port <number>`     | Port for the local OAuth callback server (default: auto 18484-18489) |

Alternatively, set `AUTH0_TV_OUTPUT=json` in the environment instead of passing `--json` on every call.

## Authentication & setup

### login

Authenticate with Auth0 via browser-based PKCE flow. **Requires human interaction** (opens browser).

```bash
auth0-tv login
auth0-tv login --reconfigure   # re-prompt for Auth0 credentials
auth0-tv --port 18486 login    # bind callback server to a specific port
```

| Flag            | Description                                       |
| --------------- | ------------------------------------------------- |
| `--reconfigure` | Re-prompt for Auth0 domain, client ID, and secret |

### logout

Clear all stored credentials and disconnect all services.

```bash
auth0-tv --json logout
auth0-tv --json logout --local   # clear local credentials only
auth0-tv --json --port 18486 logout
```

| Flag      | Description                                                     |
| --------- | --------------------------------------------------------------- |
| `--local` | Only clear local credentials without ending the browser session |

### status

Show current user and connected services.

```bash
auth0-tv --json status
```

Example JSON output:

```json
{
  "loggedIn": true,
  "user": { "email": "user@example.com", "name": "User Name" },
  "connections": ["google-oauth2"]
}
```

### connect

Connect a third-party service or any Auth0 connection. **Requires human interaction** (opens browser for OAuth).

Known services (gmail, calendar, github, slack) have default scopes and allowed domains. Any other name is treated as a custom Auth0 connection — the input string is used directly as the connection identifier sent to Auth0.

```bash
# Known services
auth0-tv connect gmail
auth0-tv --port 18486 connect gmail
auth0-tv connect github --allowed-domains "api.github.com,ghcr.io"
auth0-tv connect gmail --scopes "https://www.googleapis.com/auth/gmail.labels"

# Custom Auth0 connections (any connection configured on your tenant)
auth0-tv connect my-enterprise-idp --scopes "openid,profile" --allowed-domains "api.example.com"
auth0-tv connect google-oauth2 --scopes "https://www.googleapis.com/auth/drive.readonly" --allowed-domains "*.googleapis.com"
```

| Flag                       | Description                                                                  |
| -------------------------- | ---------------------------------------------------------------------------- |
| `--allowed-domains <list>` | Comma-separated domains allowed for `auth0-tv fetch` (additive)              |
| `--scopes <list>`          | Comma-separated extra scopes to request (merged with service default scopes) |

Known services have default allowed domains and scopes built in. Custom connections have no defaults — use `--scopes` and `--allowed-domains` to configure them.

Use `--scopes` to request additional OAuth scopes beyond the service defaults (e.g. for API endpoints not covered by the built-in scope set). Extra scopes are merged and deduplicated with the service's default scopes and any existing remote scopes.

### disconnect

Disconnect a third-party service or custom connection. By default, only removes the locally-cached token. Use `--remote` to also remove the server-side connection from Auth0 Token Vault.

```bash
auth0-tv --json disconnect gmail
auth0-tv --json disconnect gmail --remote
auth0-tv --json disconnect my-enterprise-idp
```

| Flag       | Description                                                |
| ---------- | ---------------------------------------------------------- |
| `--remote` | Also remove the server-side connection (Auth0 Token Vault) |

Example JSON output (local only):

```json
{ "status": "disconnected", "service": "gmail", "remote": false }
```

Example JSON output (with `--remote`):

```json
{ "status": "disconnected", "service": "gmail", "remote": true }
```

### connections

List connected services. When logged in, fetches remote connected accounts from Auth0 and shows the local token status for each. Falls back to local-only listing when not logged in or if the remote API is unreachable.

```bash
auth0-tv --json connections
```

Example JSON output (logged in, remote available):

```json
{
  "connections": [
    {
      "connection": "google-oauth2",
      "service": "gmail",
      "id": "ca_abc123",
      "scopes": ["https://www.googleapis.com/auth/gmail.modify"],
      "tokenStatus": "valid",
      "remote": true
    },
    {
      "connection": "slack",
      "service": "slack",
      "id": "ca_def456",
      "scopes": ["chat:write"],
      "tokenStatus": "none",
      "remote": true
    }
  ]
}
```

The `tokenStatus` field indicates local token availability:

- `valid` — local token is cached and not expired
- `expired` — local token is cached but expired
- `none` — no local token (remote-only connection)

The `remote` field indicates whether the entry came from the Auth0 server (`true`) or from local cache only (`false`, when not logged in).

## Gmail commands

All Gmail commands require a connected Gmail account. If not connected, the CLI exits with code 4.

### gmail search

Search messages using Gmail search syntax.

```bash
auth0-tv --json gmail search "from:boss@company.com is:unread"
auth0-tv --json gmail search "meeting notes" -n 5
auth0-tv --json gmail search "in:inbox" --page-token <token>
```

| Flag                    | Description               | Default |
| ----------------------- | ------------------------- | ------- |
| `-n, --max-results <n>` | Maximum results to return | 10      |
| `--page-token <token>`  | Page token for pagination | —       |

### gmail read

Read a message by ID.

```bash
auth0-tv --json gmail read <messageId>
```

### gmail send

Send a new message. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm gmail send --to user@example.com --subject "Subject" --body "Body text"
auth0-tv --json --confirm gmail send --to user@example.com --subject "Subject" --body-file ./message.txt
echo "Body" | auth0-tv --json --confirm gmail send --to user@example.com --subject "Subject"
```

| Flag                  | Description                        |
| --------------------- | ---------------------------------- |
| `--to <address>`      | Recipient email address (required) |
| `--subject <subject>` | Email subject (required)           |
| `--body <text>`       | Email body text                    |
| `--body-file <path>`  | Read body from file                |

Body can also be provided via stdin when neither `--body` nor `--body-file` is specified.

### gmail reply

Reply to a message. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm gmail reply <messageId> --body "Thanks!"
auth0-tv --json --confirm gmail reply <messageId> --body-file ./reply.txt
```

| Flag                 | Description         |
| -------------------- | ------------------- |
| `--body <text>`      | Reply body text     |
| `--body-file <path>` | Read body from file |

### gmail forward

Forward a message. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm gmail forward <messageId> --to recipient@example.com
```

| Flag             | Description                        |
| ---------------- | ---------------------------------- |
| `--to <address>` | Recipient email address (required) |

### gmail archive

Archive a message (remove from inbox). **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm gmail archive <messageId>
```

### gmail delete

Move a message to trash. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm gmail delete <messageId>
```

### gmail labels

List all labels.

```bash
auth0-tv --json gmail labels
```

### gmail label

Add or remove labels from a message.

```bash
auth0-tv --json gmail label <messageId> --add STARRED
auth0-tv --json gmail label <messageId> --remove INBOX --add ARCHIVED
auth0-tv --json gmail label <messageId> --add "Label_1,Label_2"
```

| Flag                | Description                         |
| ------------------- | ----------------------------------- |
| `--add <labels>`    | Comma-separated label IDs to add    |
| `--remove <labels>` | Comma-separated label IDs to remove |

### gmail draft create

Create a new draft.

```bash
auth0-tv --json gmail draft create --to user@example.com --subject "Draft" --body "Content"
auth0-tv --json gmail draft create --to user@example.com --subject "Draft" --body-file ./draft.txt
```

| Flag                  | Description             |
| --------------------- | ----------------------- |
| `--to <address>`      | Recipient email address |
| `--subject <subject>` | Email subject           |
| `--body <text>`       | Draft body text         |
| `--body-file <path>`  | Read body from file     |

### gmail draft list

List drafts.

```bash
auth0-tv --json gmail draft list
auth0-tv --json gmail draft list -n 5
```

| Flag                    | Description     | Default |
| ----------------------- | --------------- | ------- |
| `-n, --max-results <n>` | Maximum results | 20      |

### gmail draft send

Send an existing draft. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm gmail draft send <draftId>
```

### gmail draft delete

Delete a draft. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm gmail draft delete <draftId>
```

## Google Calendar commands

All Calendar commands require a connected Google Calendar account. If not connected, the CLI exits with code 4.

### calendar list

List calendars the user has access to.

```bash
auth0-tv --json calendar list
auth0-tv --json calendar list --max-results 5
```

| Flag                | Description               | Default |
| ------------------- | ------------------------- | ------- |
| `--max-results <n>` | Maximum results to return | 100     |

### calendar events

List events from a calendar.

```bash
auth0-tv --json calendar events
auth0-tv --json calendar events primary --from 2026-03-28T00:00:00Z --to 2026-04-04T00:00:00Z
auth0-tv --json calendar events --query "standup" --max-results 5
```

| Flag                   | Description               | Default   |
| ---------------------- | ------------------------- | --------- |
| `[calendarId]`         | Calendar ID               | `primary` |
| `--from <date>`        | Start date (ISO 8601)     | —         |
| `--to <date>`          | End date (ISO 8601)       | —         |
| `--query <text>`       | Free-text search          | —         |
| `--max-results <n>`    | Maximum results to return | 25        |
| `--page-token <token>` | Page token for pagination | —         |

### calendar get

Get details for a specific event.

```bash
auth0-tv --json calendar get <eventId>
auth0-tv --json calendar get <eventId> --calendar <calendarId>
```

| Flag              | Description | Default   |
| ----------------- | ----------- | --------- |
| `--calendar <id>` | Calendar ID | `primary` |

### calendar create

Create a new event. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm calendar create --summary "Meeting" --start 2026-03-28T10:00:00 --end 2026-03-28T11:00:00
auth0-tv --json --confirm calendar create --summary "Lunch" --start 2026-03-28T12:00:00 --end 2026-03-28T13:00:00 --location "Cafe" --attendees "a@b.com,c@d.com" --description "Team lunch"
```

| Flag                   | Description                      |
| ---------------------- | -------------------------------- |
| `--summary <text>`     | Event title (required)           |
| `--start <datetime>`   | Start time, ISO 8601 (required)  |
| `--end <datetime>`     | End time, ISO 8601 (required)    |
| `--location <text>`    | Event location                   |
| `--description <text>` | Event description                |
| `--attendees <emails>` | Comma-separated attendee emails  |
| `--calendar <id>`      | Calendar ID (default: `primary`) |

### calendar update

Update an existing event. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm calendar update <eventId> --summary "New Title"
auth0-tv --json --confirm calendar update <eventId> --start 2026-03-28T14:00:00 --end 2026-03-28T15:00:00
```

All fields are optional — only provided fields are updated (uses PATCH).

| Flag                   | Description                      |
| ---------------------- | -------------------------------- |
| `--summary <text>`     | Event title                      |
| `--start <datetime>`   | Start time, ISO 8601             |
| `--end <datetime>`     | End time, ISO 8601               |
| `--location <text>`    | Event location                   |
| `--description <text>` | Event description                |
| `--attendees <emails>` | Comma-separated attendee emails  |
| `--calendar <id>`      | Calendar ID (default: `primary`) |

### calendar delete

Delete an event. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm calendar delete <eventId>
auth0-tv --json --confirm calendar delete <eventId> --calendar <calendarId>
```

| Flag              | Description                      |
| ----------------- | -------------------------------- |
| `--calendar <id>` | Calendar ID (default: `primary`) |

### calendar quick-add

Create an event using natural language. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm calendar quick-add "Lunch with Alice tomorrow at noon at Cafe Nero"
```

| Flag              | Description                      |
| ----------------- | -------------------------------- |
| `--calendar <id>` | Calendar ID (default: `primary`) |

## Slack commands

All Slack commands require a connected Slack account. If not connected, the CLI exits with code 4.

### slack channels

List Slack channels the user is in.

```bash
auth0-tv --json slack channels
auth0-tv --json slack channels --limit 50
```

| Flag               | Description              | Default |
| ------------------ | ------------------------ | ------- |
| `--limit <n>`      | Maximum results per page | 100     |
| `--cursor <token>` | Pagination cursor        | —       |

### slack messages

List messages in a channel.

```bash
auth0-tv --json slack messages C1234567890
auth0-tv --json slack messages C1234567890 --limit 20 --oldest 1609459200
```

| Flag               | Description                   | Default |
| ------------------ | ----------------------------- | ------- |
| `--limit <n>`      | Maximum messages per page     | 50      |
| `--cursor <token>` | Pagination cursor             | —       |
| `--oldest <ts>`    | Start of time range (Unix ts) | —       |
| `--latest <ts>`    | End of time range (Unix ts)   | —       |

### slack search

Search Slack messages. Supports Slack search syntax (`from:@user`, `in:#channel`, `has:link`, etc.).

```bash
auth0-tv --json slack search "project update"
auth0-tv --json slack search "from:@alice in:#general" --count 5
```

| Flag               | Description                     | Default     |
| ------------------ | ------------------------------- | ----------- |
| `--sort <field>`   | Sort by `timestamp` or `score`  | `timestamp` |
| `--sort-dir <dir>` | Sort direction: `asc` or `desc` | `desc`      |
| `--count <n>`      | Results per page (max 100)      | 20          |
| `--page <n>`       | Page number (1-indexed)         | 1           |

### slack post

Post a message to a channel. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm slack post C1234567890 --text "Hello team!"
```

| Flag           | Description             |
| -------------- | ----------------------- |
| `--text <msg>` | Message text (required) |

### slack reply

Reply to a thread. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm slack reply C1234567890 1234567890.123456 --text "Got it!"
```

| Flag           | Description           |
| -------------- | --------------------- |
| `--text <msg>` | Reply text (required) |

### slack react

Add or remove an emoji reaction on a message.

```bash
auth0-tv --json slack react C1234567890 1234567890.123456 --add thumbsup
auth0-tv --json slack react C1234567890 1234567890.123456 --remove thumbsup
```

| Flag               | Description                      |
| ------------------ | -------------------------------- |
| `--add <emoji>`    | Emoji name to add (no colons)    |
| `--remove <emoji>` | Emoji name to remove (no colons) |

### slack users

List Slack users.

```bash
auth0-tv --json slack users
auth0-tv --json slack users --limit 50
```

| Flag               | Description              | Default |
| ------------------ | ------------------------ | ------- |
| `--limit <n>`      | Maximum results per page | 200     |
| `--cursor <token>` | Pagination cursor        | —       |

### slack user

Get info about a specific Slack user.

```bash
auth0-tv --json slack user U1234567890
```

### slack status

Set your Slack status.

```bash
auth0-tv --json slack status --text "In a meeting" --emoji ":calendar:" --expiration 60
```

| Flag                  | Description                              |
| --------------------- | ---------------------------------------- |
| `--text <text>`       | Status text (required)                   |
| `--emoji <emoji>`     | Status emoji (e.g. `:calendar:`)         |
| `--expiration <mins>` | Minutes until status expires (0 = never) |

## GitHub commands

All GitHub commands require a connected GitHub account. If not connected, the CLI exits with code 4.

### github repos

List your GitHub repositories.

```bash
auth0-tv --json github repos
auth0-tv --json github repos --limit 10 --sort stars --type all
```

| Flag              | Description                                      | Default   |
| ----------------- | ------------------------------------------------ | --------- |
| `-n, --limit <n>` | Maximum repos to return                          | 30        |
| `--sort <field>`  | Sort by field (created/updated/pushed/full_name) | `updated` |
| `--type <type>`   | Filter by type (all/owner/member)                | `owner`   |

### github repo

Get details of a specific repository.

```bash
auth0-tv --json github repo octocat/Hello-World
```

### github issues

List issues for a repository.

```bash
auth0-tv --json github issues octocat/Hello-World
auth0-tv --json github issues octocat/Hello-World --state closed --labels "bug,enhancement"
```

| Flag                | Description                       | Default |
| ------------------- | --------------------------------- | ------- |
| `--state <state>`   | Filter by state (open/closed/all) | `open`  |
| `-n, --limit <n>`   | Maximum issues to return          | 30      |
| `--labels <labels>` | Comma-separated label filter      | —       |

### github issue get

Get details of a specific issue.

```bash
auth0-tv --json github issue get octocat/Hello-World 42
```

### github issue create

Create a new issue. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm github issue create octocat/Hello-World --title "Bug report" --body "Steps to reproduce..."
auth0-tv --json --confirm github issue create octocat/Hello-World --title "Feature" --labels "enhancement" --assignees "octocat"
```

| Flag                      | Description               |
| ------------------------- | ------------------------- |
| `--title <title>`         | Issue title (required)    |
| `--body <body>`           | Issue body                |
| `--labels <labels>`       | Comma-separated labels    |
| `--assignees <assignees>` | Comma-separated assignees |

### github issue comment

Add a comment to an issue. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm github issue comment octocat/Hello-World 42 --body "Looks good!"
```

| Flag            | Description             |
| --------------- | ----------------------- |
| `--body <body>` | Comment body (required) |

### github issue close

Close an issue. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm github issue close octocat/Hello-World 42
```

### github prs

List pull requests for a repository.

```bash
auth0-tv --json github prs octocat/Hello-World
auth0-tv --json github prs octocat/Hello-World --state all --limit 10
```

| Flag              | Description                       | Default |
| ----------------- | --------------------------------- | ------- |
| `--state <state>` | Filter by state (open/closed/all) | `open`  |
| `-n, --limit <n>` | Maximum pull requests to return   | 30      |

### github pr get

Get details of a specific pull request.

```bash
auth0-tv --json github pr get octocat/Hello-World 42
```

### github pr comment

Add a comment to a pull request. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm github pr comment octocat/Hello-World 42 --body "LGTM!"
```

| Flag            | Description             |
| --------------- | ----------------------- |
| `--body <text>` | Comment body (required) |

### github notifications

List your GitHub notifications.

```bash
auth0-tv --json github notifications
auth0-tv --json github notifications --all --limit 50
```

| Flag              | Description                     | Default |
| ----------------- | ------------------------------- | ------- |
| `--all`           | Include read notifications      | false   |
| `-n, --limit <n>` | Maximum notifications to return | 30      |

### github notification read

Mark a notification as read. **Destructive — requires `--confirm`.**

```bash
auth0-tv --json --confirm github notification read <notificationId>
```

### github search repos

Search GitHub repositories.

```bash
auth0-tv --json github search repos "auth0 language:typescript"
auth0-tv --json github search repos "cli" --sort stars --limit 10
```

| Flag              | Description                         | Default |
| ----------------- | ----------------------------------- | ------- |
| `-n, --limit <n>` | Maximum results to return           | 20      |
| `--sort <field>`  | Sort by field (stars/forks/updated) | —       |

### github search code

Search code across GitHub.

```bash
auth0-tv --json github search code "handleError repo:octocat/Hello-World"
```

| Flag              | Description               | Default |
| ----------------- | ------------------------- | ------- |
| `-n, --limit <n>` | Maximum results to return | 20      |

### github search issues

Search issues and pull requests.

```bash
auth0-tv --json github search issues "bug label:critical"
auth0-tv --json github search issues "auth0" --sort comments --limit 10
```

| Flag              | Description                              | Default |
| ----------------- | ---------------------------------------- | ------- |
| `-n, --limit <n>` | Maximum results to return                | 20      |
| `--sort <field>`  | Sort by field (created/updated/comments) | —       |

## API passthrough (fetch)

Make an authenticated HTTP request to an allowed domain using a service or custom connection token. Only HTTPS URLs are permitted.

### fetch

```bash
# Known services
auth0-tv --json fetch github https://api.github.com/user
auth0-tv --json fetch gmail https://gmail.googleapis.com/gmail/v1/users/me/messages -X GET
auth0-tv --json fetch slack https://slack.com/api/conversations.list
auth0-tv --json fetch github https://api.github.com/repos/octocat/Hello-World/issues -X POST -d '{"title":"Bug"}'
auth0-tv --json fetch github https://api.github.com/user -H "Accept: application/vnd.github.v3+json"
auth0-tv --json fetch slack https://slack.com/api/chat.postMessage -X POST --data-file ./payload.json

# Custom connections (requires --allowed-domains set during connect)
auth0-tv --json fetch my-enterprise-idp https://api.example.com/users/me
```

| Flag                    | Description                    | Default |
| ----------------------- | ------------------------------ | ------- |
| `-X, --method <method>` | HTTP method                    | `GET`   |
| `-H, --header <header>` | Additional header (repeatable) | —       |
| `-d, --data <body>`     | Request body (inline)          | —       |
| `--data-file <path>`    | Read request body from file    | —       |

**Default allowed domains per service:**

| Service    | Default allowed domains    |
| ---------- | -------------------------- |
| `gmail`    | `*.googleapis.com`         |
| `calendar` | `*.googleapis.com`         |
| `github`   | `api.github.com`           |
| `slack`    | `slack.com`, `*.slack.com` |

Additional domains can be added with `auth0-tv connect <service> --allowed-domains <list>`. For known services, custom domains are merged with the defaults. Custom connections have no default domains — `--allowed-domains` must be set during `connect` for `fetch` to work.

The `Authorization: Bearer <token>` header is added automatically. You can add extra headers with `-H`.

## Exit codes

| Code | Constant              | Meaning                                                            |
| ---- | --------------------- | ------------------------------------------------------------------ |
| 0    | —                     | Success                                                            |
| 1    | `EXIT_GENERAL`        | General / unexpected error                                         |
| 2    | `EXIT_INVALID_INPUT`  | Invalid input or missing required flag                             |
| 3    | `EXIT_AUTH_REQUIRED`  | Authentication required — user must run `auth0-tv login`           |
| 4    | `EXIT_AUTHZ_REQUIRED` | Service not connected — user must run `auth0-tv connect <service>` |
| 5    | `EXIT_SERVICE_ERROR`  | Upstream service error (e.g. Gmail API failure)                    |
| 6    | `EXIT_NETWORK_ERROR`  | Network error (unreachable host, timeout)                          |

## Error JSON format

When `--json` is active, errors are returned as structured JSON to stdout:

```json
{
  "error": {
    "code": "token_exchange_error",
    "message": "Service not connected. Run `auth0-tv connect gmail` first."
  }
}
```
