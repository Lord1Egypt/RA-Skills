---
name: flowus-cli
description: Use when an agent needs to call the FlowUs API through the FlowUs CLI, authenticate FlowUs, upload a file, create or update a page, query a database, search content, edit Markdown page content, or any task involving the `flowus` command.
metadata:
  openclaw:
    envVars:
      - name: FLOWUS_TOKEN
        required: false
        description: Optional FlowUs bearer token; browser login or saved CLI credentials may be used instead.
      - name: FLOWUS_BASE_URL
        required: false
        description: Optional FlowUs API base URL.
      - name: FLOWUS_CONFIG_DIR
        required: false
        description: Optional directory containing FlowUs CLI credentials and configuration.
      - name: FLOWUS_USER_AGENT
        required: false
        description: Optional suffix for the FlowUs CLI user agent.
---

# FlowUs CLI

Use the FlowUs CLI (`flowus`) for FlowUs V2 API work: pages, blocks,
databases, search, Markdown content, and files.

The CLI source repository may be private. Do not ask the user to clone source
code before using the CLI. Install or update the released binary from the
official FlowUs CDN only after the user explicitly approves it.

## Mandatory preflight

Complete this preflight before a remote FlowUs API call. CLI help, endpoint
documentation, and offline planning do not require authentication.

1. Inspect whether the CLI is available without installing or updating it:

```bash
if command -v flowus >/dev/null 2>&1; then
  flowus version
else
  echo "FlowUs CLI is not installed"
fi
```

If the CLI is missing or outdated, explain that the official installer is
available at `https://cdn2.flowus.cn/flowus-cli/install` (or
`https://cdn2.flowus.cn/flowus-cli/install.ps1` on Windows). Do not download,
execute, or update it until the user explicitly approves that action.

After approval, use only the official URL and a user-approved version. Download
an installer to a temporary file; show its source, version, and SHA-256 hash;
and compare it with an official checksum or signature before execution. If no
official integrity data is available, stop and offer manual installation rather
than executing an unverified installer. Remove temporary installer files after
the attempt.

2. If the CLI is installed, inspect authentication and active identity:

```bash
flowus --json doctor
flowus --json whoami
```

Continue only when the checks show authenticated FlowUs credentials. If
authentication is missing or invalid, do not start a login flow automatically.
Explain the available options and wait for the user's explicit choice:

- If `FLOWUS_TOKEN` is already set, rerun `flowus --json doctor` and
  `flowus --json whoami`; do not ask for another login.
- Browser login: `flowus login --browser`.
- Manual setup for headless environments: `flowus --json login --manual`.
- Configure `FLOWUS_TOKEN` or saved credentials through an approved secret
  channel.

Do not run plain `flowus login` in agent sessions because it can block on an
interactive method prompt. Do not make API calls or draw conclusions from
incomplete data until authentication is verified. After the user explicitly
approves a login method, run only that selected method and then rerun
`flowus --json doctor` and `flowus --json whoami`.

Use this browser login command only after the user explicitly selects browser
login:

```bash
flowus login --browser
```

Use manual setup only after the user explicitly selects it for a headless or
remote environment:

```bash
flowus --json login --manual
```

If a command is missing or help output looks stale, explain that `flowus update`
can update the CLI and wait for explicit user approval before running it.

Useful install overrides:

- `FLOWUS_INSTALL_DIR` - install directory.
- `FLOWUS_VERSION` - exact release version, such as `v0.1.10`.
- `FLOWUS_CLI_RELEASE_BASE_URL` - alternate release base URL for tests.

## First rule: ask the CLI

The CLI is self-documenting. Prefer these commands over guessing syntax or
request fields:

- `flowus --help` - list global options and top-level commands.
- `flowus help <command...>` - show usage, options, examples, and notes for any
  command or subcommand.
- `flowus api ls` - list public API endpoints and request field hints.
- `flowus api ls --plain` - compact endpoint list for scanning.
- `flowus api --docs <PATH> -X <METHOD>` - show agent-readable Markdown docs
  for one endpoint, including parameters, examples, and safety notes.
- `flowus api --spec <PATH> -X <METHOD>` - show the exact embedded OpenAPI
  fragment for one endpoint.
- `flowus --json doctor` - inspect local authentication and configuration state
  when auth or base URL selection is unclear.
- `flowus --json whoami` - verify the active FlowUs identity.
- `flowus markdown get <page-id>` - retrieve page content as Markdown.

If you are unsure about syntax, request body fields, pagination, auth source,
or command coverage, run help first.

## Credentials and configuration

The CLI resolves credentials in this precedence order:

1. `--token <token>`
2. `FLOWUS_TOKEN`
3. saved login credentials in the FlowUs credential store

This is CLI resolution behavior, not authorization to expose a credential. Do
not pass `--token` in agent commands, logs, or shared shells: it can leak via
process listings or shell history. Do not ask users to paste bearer tokens into
chat. Use preconfigured `FLOWUS_TOKEN`, saved credentials, or an approved secret
channel; redact any credential that appears in command output.

If no valid credentials are available, offer browser login, manual setup, or an
approved secret path and wait for the user to select one. After the selected
login succeeds, rerun `flowus --json doctor` and `flowus --json whoami`.

If `flowus --json doctor`, `flowus --json whoami`, or an API command reports an
authentication failure (including HTTP 401), treat the active credential as
invalid or expired. Check whether `--token` or `FLOWUS_TOKEN` is overriding
saved credentials. Have the user update or remove an invalid override through
an approved secret path, then offer the login or credential path above and wait
for their explicit choice. Do not retry API work until `doctor` and `whoami`
verify authentication.

Common environment variables:

- `FLOWUS_TOKEN` - bearer token for API calls.
- `FLOWUS_BASE_URL` - API base URL; default is `https://api.flowus.cn`.
- `FLOWUS_CONFIG_DIR` - config directory; default follows the FlowUs profile.
- `FLOWUS_USER_AGENT` - custom user agent suffix.

Do not print bearer tokens, write them into files, or paste them into request
bodies. Do not call the FlowUs V2 API with `curl`; use the CLI so auth,
product defaults, retries, and error formatting stay consistent.

## Working rules

- Use `--json` for stable machine-readable stdout.
- Keep JSON request bodies in local files and pass them with `--body <file>`.
- Keep Markdown replacement content in local files and pass it with `--file <file>`.
- Prefer domain commands over `api call`; `flowus api --docs` names a
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
flowus --json page get <page_id>
flowus markdown get <page_id> > page.md
```

Use Markdown for page content work whenever possible. It is easier to inspect,
edit, and diff than raw block JSON.

### Replace page Markdown

```bash
flowus markdown put --file page.md <page_id>
```

Only run this after confirming the target page ID and replacement file.

### Create or update a page with JSON

Create a local JSON body file, then pass it to the CLI:

```bash
flowus --json page create --body page.json
flowus --json page update --body patch.json <page_id>
```

For idempotent creates, use `--idempotency-key <key>`.

### Blocks and children

```bash
flowus --json block get <block_id>
flowus --json block children <block_id>
flowus --json block append <block_id> --body children.json
flowus --json block update <block_id> --body block-patch.json
```

### Databases

```bash
flowus --json database get <database_id>
flowus --json database query <database_id> --body query.json
flowus --json database mutate <database_id> --body mutation.json --idempotency-key <key>
flowus --json page property get <page_id> <property_id>
```

Use `flowus api --docs` or command help to inspect filter and sort body shapes
before writing `query.json`.

Use `database mutate` for one atomic, permission-checked database write. Read
the database first; use stable property IDs for changes; use a stable idempotency
key; and never overwrite existing records when the user asked to create records.
Use `flowus api --docs` to obtain the exact body shape.

### Search

```bash
flowus --json search text "roadmap" --page-size 10
flowus --json search semantic "tasks about quarterly planning" --space-id <space_id> --page-size 10
```

Use text search for exact titles, keywords, and known phrases. Use semantic
search when intent matters more than exact wording.

### Files

Upload a local file for a parent page:

```bash
flowus --json file upload --parent-page <page_id> ./report.pdf
```

Append a FlowUs-hosted file block with the returned object name and size:

```bash
flowus --json block append-file <block_id> --oss-name <oss_name> --size <bytes>
```

Append an external file URL:

```bash
flowus --json block append-file <block_id> --external-url https://example.com/report.pdf
```

## Fallback API calls

Use `api call` only when no domain command covers the endpoint. Lookup sequence:

```bash
flowus api ls --plain
flowus api --docs /v2/blocks/{block_id}/children -X PATCH
flowus api --spec /v2/blocks/{block_id}/children -X PATCH
flowus --json api call PATCH /v2/blocks/:block_id/children --param block_id=<block_id> --body body.json
```

For `POST`, `PUT`, or `PATCH`, read `--docs` and `--spec` first and apply the
write-safety rules above. `--param` fills path placeholders first; remaining
keys become query parameters. Use `--header NAME=VALUE` only for non-secret
headers such as `If-Match`; never put credentials or sessions in headers.

## Troubleshooting

- Command not found: offer the official installer at `https://cdn2.flowus.cn/flowus-cli/install` and wait for explicit approval before using it.
- Unknown command or option: ask approval before running `flowus update`, then run `flowus <command> --help`.
- Authentication failure or HTTP 401: follow the invalid/expired credential
  recovery rule above; do not retry API work until `doctor` and `whoami` verify
  authentication.
- Unexpected API shape: run `flowus api --docs <PATH> -X <METHOD>` and
  `flowus api --spec <PATH> -X <METHOD>` before retrying.
