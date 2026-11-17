# Safety Policy

Default to least privilege. Add power only when the user confirms it.

## Default Deny

Require approval for:

- shell commands that modify files, install packages, start external services, or access secrets
- file writes outside the target project
- deletes and recursive moves
- database writes or migrations
- browser automation that submits forms or changes account state
- external API mutation
- network calls with cost, quota, or account impact

## Dry Run

Use dry-run mode when available for:

- destructive filesystem actions
- package publishing
- infrastructure changes
- bulk data updates
- outbound notifications

## Credentials

- Never commit real API keys, tokens, cookies, or secrets.
- Use `.env.example` for variable names and comments only.
- Load real secrets from environment variables or a local secret store.
- Fail clearly when required secrets are missing.

## Mock and Test Doubles

Mocks are allowed only for offline tests. Name them clearly:

- `mockProvider`
- `fakeTool`
- `testDouble`

Do not wire mocks into production execution paths unless the app has an explicit `test` mode.

