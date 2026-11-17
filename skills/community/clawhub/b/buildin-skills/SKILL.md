---
name: buildin-cli
description: Use when an agent needs to call the Buildin API through the Buildin CLI, authenticate Buildin, upload a file, create or update a page, query a database, search content, edit Markdown page content, or any task involving the `buildin` command.
metadata:
  openclaw:
    envVars:
      - name: BUILDIN_TOKEN
        required: false
        description: Optional Buildin bearer token; browser login or saved CLI credentials may be used instead.
      - name: BUILDIN_BASE_URL
        required: false
        description: Optional Buildin API base URL.
      - name: BUILDIN_CONFIG_DIR
        required: false
        description: Optional directory containing Buildin CLI credentials and configuration.
      - name: BUILDIN_USER_AGENT
        required: false
        description: Optional suffix for the Buildin CLI user agent.
---

# Buildin CLI

Use the Buildin CLI (`buildin`) for Buildin V2 API work: pages, blocks,
databases, search, Markdown content, and files.

The CLI source repository may be private. Do not ask the user to clone source
code before using the CLI. Install or update the released binary from the
official Buildin CDN only after the user explicitly approves it.

Use only the Buildin command, Buildin base URL, `BUILDIN_*` environment
variables, and Buildin credential store for Buildin work.

## Mandatory preflight

Complete this preflight before a remote Buildin API call. CLI help, endpoint
documentation, and offline planning do not require authentication.

1. Inspect whether the CLI is available without installing or updating it:

```bash
if command -v buildin >/dev/null 2>&1; then
  buildin version
else
  echo "Buildin CLI is not installed"
fi
```

If the CLI is missing or outdated, explain that the official installer is
available at `https://cdn.buildin.ai/buildin-cli/install` (or
`https://cdn.buildin.ai/buildin-cli/install.ps1` on Windows). Do not download,
execute, or update it until the user explicitly approves that action.

After approval, use only the official URL and a user-approved version. Download
an installer to a temporary file; show its source, version, and SHA-256 hash;
and compare it with an official checksum or signature before execution. If no
official integrity data is available, stop and offer manual installation rather
than executing an unverified installer. Remove temporary installer files after
the attempt.

2. If the CLI is installed, inspect authentication and active identity:

```bash
buildin --json doctor
buildin --json whoami
```

Continue only when the checks show authenticated Buildin credentials. If
authentication is missing or invalid, do not start a login flow automatically.
Explain the available options and wait for the user's explicit choice:

- If `BUILDIN_TOKEN` is already set, rerun `buildin --json doctor` and
  `buildin --json whoami`; do not ask for another login.
- Browser login: `buildin login --browser`.
- Manual setup for headless environments: `buildin --json login --manual`.
- Configure `BUILDIN_TOKEN` or saved credentials through an approved secret
  channel.

Do not run plain `buildin login` in agent sessions because it can block on an
interactive method prompt. Do not make API calls or draw conclusions from
incomplete data until authentication is verified. After the user explicitly
approves a login method, run only that selected method and then rerun
`buildin --json doctor` and `buildin --json whoami`.

Use this browser login command only after the user explicitly selects browser
login:

```bash
buildin login --browser
```

Use manual setup only after the user explicitly selects it for a headless or
remote environment:

```bash
buildin --json login --manual
```

If a command is missing or help output looks stale, explain that `buildin update`
can update the CLI and wait for explicit user approval before running it.

Useful install overrides:

- `BUILDIN_INSTALL_DIR` - install directory.
- `BUILDIN_VERSION` - exact release version, such as `v0.1.10`.
- `BUILDIN_CLI_RELEASE_BASE_URL` - alternate release base URL for tests.

## First rule: ask the CLI

The CLI is self-documenting. Prefer these commands over guessing syntax or
request fields:

- `buildin --help` - list global options and top-level commands.
- `buildin help <command...>` - show usage, options, examples, and notes for any
  command or subcommand.
- `buildin api ls` - list public API endpoints and request field hints.
- `buildin api ls --plain` - compact endpoint list for scanning.
- `buildin api --docs <PATH> -X <METHOD>` - show agent-readable Markdown docs
  for one endpoint, including parameters, examples, and safety notes.
- `buildin api --spec <PATH> -X <METHOD>` - show the exact embedded OpenAPI
  fragment for one endpoint.
- `buildin --json doctor` - inspect local authentication and configuration
  state when auth or base URL selection is unclear.
- `buildin --json whoami` - verify the active Buildin identity.
- `buildin markdown get <page-id>` - retrieve page content as Markdown.

If you are unsure about syntax, request body fields, pagination, auth source,
or command coverage, run help first.

## Credentials and configuration

The CLI resolves credentials in this precedence order:

1. `--token <token>`
2. `BUILDIN_TOKEN`
3. saved login credentials in the Buildin credential store

This is CLI resolution behavior, not authorization to expose a credential. Do
not pass `--token` in agent commands, logs, or shared shells: it can leak via
process listings or shell history. Do not ask users to paste bearer tokens into
chat. Use preconfigured `BUILDIN_TOKEN`, saved credentials, or an approved secret
channel; redact any credential that appears in command output.

If no valid credentials are available, offer browser login, manual setup, or an
approved secret path and wait for the user to select one. After the selected
login succeeds, rerun `buildin --json doctor` and `buildin --json whoami`.

If `buildin --json doctor`, `buildin --json whoami`, or an API command reports
an authentication failure (including HTTP 401), treat the active credential as
invalid or expired. Check whether `--token` or `BUILDIN_TOKEN` is overriding
saved credentials. Have the user update or remove an invalid override through
an approved secret path, then offer the login or credential path above and wait
for their explicit choice. Do not retry API work until `doctor` and `whoami`
verify authentication.

Common environment variables:

- `BUILDIN_TOKEN` - bearer token for API calls.
- `BUILDIN_BASE_URL` - API base URL; default is `https://api.buildin.ai`.
- `BUILDIN_CONFIG_DIR` - config directory; default follows the Buildin profile.
- `BUILDIN_USER_AGENT` - custom user agent suffix.

Do not print bearer tokens, write them into files, or paste them into request
bodies. Do not call the Buildin V2 API with `curl`; use the CLI so auth,
product defaults, retries, and error formatting stay consistent.

## Working rules

- Use `--json` for stable machine-readable stdout.
- Keep JSON request bodies in local files and pass them with `--body <file>`.
- Keep Markdown replacement content in local files and pass it with `--file <file>`.
- Prefer domain commands over `api call`; `buildin api --docs` names a
  recommended domain command when one exists.
- For paginated commands, inspect JSON output for cursors and repeat with the
  command's cursor option.

## Write safety

Before any remote create, update, append, upload, replace, or raw API write:

1. Confirm the exact target, operation, and expected impact (including record
   count, affected blocks, or uploaded files).
2. Read the current target first when feasible. For a Markdown replacement,
   compare the existing content unless the user explicitly authorized a full
   replacement. Use `--if-match` when the CLI exposes a version or ETag.
3. If the user did not provide both an exact target and the intended content,
   present a short change summary and wait for confirmation.
4. Confirm files and external URLs are user-authorized and do not contain
   credentials or private data not intended for the target workspace.

The CLI intentionally rejects DELETE API calls. This Skill does not execute or
suggest bypasses; use a dedicated deletion workflow with a second confirmation.

## Common workflows

### Read a page

```bash
buildin --json page get <page_id>
buildin markdown get <page_id> > page.md
```

Use Markdown for page content work whenever possible. It is easier to inspect,
edit, and diff than raw block JSON.

### Replace page Markdown

```bash
buildin markdown put --file page.md <page_id>
```

Only run this after confirming the target page ID and replacement file.

### Create or update a page with JSON

Create a local JSON body file, then pass it to the CLI:

```bash
buildin --json page create --body page.json
buildin --json page update --body patch.json <page_id>
```

For idempotent creates, use `--idempotency-key <key>`.

### Blocks and children

```bash
buildin --json block get <block_id>
buildin --json block children <block_id>
buildin --json block append <block_id> --body children.json
buildin --json block update <block_id> --body block-patch.json
```

### Databases

```bash
buildin --json database get <database_id>
buildin --json database query <database_id> --body query.json
buildin --json database create --body database.json
buildin --json database update <database_id> --body patch.json
buildin --json page property get <page_id> <property_id>
```

Use `buildin api --docs` or command help to inspect filter and sort body shapes
before writing `query.json`.

### Search

```bash
buildin --json search text "roadmap" --page-size 10
buildin --json search semantic "tasks about quarterly planning" --space-id <space_id> --page-size 10
```

Use text search for exact titles, keywords, and known phrases. Use semantic
search when intent matters more than exact wording.

### Files

Upload a local file for a parent page:

```bash
buildin --json file upload --parent-page <page_id> ./report.pdf
```

Append a Buildin-hosted file block with the returned object name and size:

```bash
buildin --json block append-file <block_id> --oss-name <oss_name> --size <bytes>
```

Append an external file URL:

```bash
buildin --json block append-file <block_id> --external-url https://example.com/report.pdf
```

## Fallback API calls

Use `api call` only when no domain command covers the endpoint. Lookup sequence:

```bash
buildin api ls --plain
buildin api --docs /v2/blocks/{block_id}/children -X PATCH
buildin api --spec /v2/blocks/{block_id}/children -X PATCH
buildin --json api call PATCH /v2/blocks/:block_id/children --param block_id=<block_id> --body body.json
```

For `POST`, `PUT`, or `PATCH`, read `--docs` and `--spec` first and apply the
write-safety rules above. `--param` fills path placeholders first; remaining
keys become query parameters. Use `--header NAME=VALUE` only for non-secret
headers such as `If-Match`; never put credentials or sessions in headers.

## Troubleshooting

- Command not found: offer the official installer at `https://cdn.buildin.ai/buildin-cli/install` and wait for explicit approval before using it.
- Unknown command or option: ask approval before running `buildin update`, then run `buildin <command> --help`.
- Authentication failure or HTTP 401: follow the invalid/expired credential
  recovery rule above; do not retry API work until `doctor` and `whoami` verify
  authentication.
- Unexpected API shape: run `buildin api --docs <PATH> -X <METHOD>` and
  `buildin api --spec <PATH> -X <METHOD>` before retrying.
