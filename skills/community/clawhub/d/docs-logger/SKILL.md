---
name: docs-logger
description: Google Docs Log Automation — Append log lines to auto-created daily documents in Google Drive by PortEden Secure Access.
homepage: https://porteden.com
metadata: {"openclaw":{"emoji":"📝","requires":{"bins":["porteden"],"env":["PE_API_KEY"]},"primaryEnv":"PE_API_KEY","install":[{"id":"brew","kind":"brew","formula":"porteden/tap/porteden","bins":["porteden"],"label":"Install porteden (brew)"},{"id":"go","kind":"go","module":"github.com/porteden/cli/cmd/porteden@latest","bins":["porteden"],"label":"Install porteden (go)"}]}}
---

# porteden docs-logger

Append log lines to daily Google Docs — one document per day, auto-created inside a `PE_Logs` folder. Works like a cloud-native `.txt` log file that agents can write to from anywhere. **Use `-jc` flags** for AI-optimized output.

If `porteden` is not installed: `brew install porteden/tap/porteden` (or `go install github.com/porteden/cli/cmd/porteden@latest`).

## Setup

### 1. Authenticate (once)

- **Browser login (recommended):** `porteden auth login` — opens browser, credentials stored in system keyring
- **Direct token:** `porteden auth login --token <key>` — stored in system keyring
- **Verify:** `porteden auth status`
- If `PE_API_KEY` is set in the environment, the CLI uses it automatically (no login needed).
- Drive access requires a token with `driveAccessEnabled: true` and a connected Google account with Drive scopes.

### 2. Set the log folder (one-time)

**If `PE_LOG_FOLDER` is already set**, skip to the logging workflow — the folder is configured.

**If `PE_LOG_FOLDER` is not set**, search for an existing `PE_Logs` folder:

```bash
porteden drive files --name "PE_Logs" --mime-type application/vnd.google-apps.folder -jc
```

**If found**, copy the `id` field and set it:

```bash
export PE_LOG_FOLDER="google:0B7_FOLDER_ID..."
```

**If not found**, create the folder:

```bash
porteden drive mkdir --name "PE_Logs" -jc
```

Copy the `id` from the response and set it:

```bash
export PE_LOG_FOLDER="google:0B7_FOLDER_ID..."
```

To persist across sessions, add to your shell profile (`~/.bashrc`, `~/.zshrc`) or `.env` file. Once set, this step does not need to be repeated.

## Logging workflow (per run)

Each run appends log lines to **today's document**. Follow these two steps every time you need to log.

### Step 1. Find or create today's doc

Search for a doc named with today's date (YYYY-MM-DD) inside the log folder:

```bash
porteden drive files --name "2025-01-15" --folder $PE_LOG_FOLDER --mime-type application/vnd.google-apps.document -jc
```

**If found**, use the `id` from the result as the doc ID for step 2.

**If not found**, create today's doc:

```bash
porteden docs create --name "2025-01-15" --folder $PE_LOG_FOLDER -jc
```

Use the `id` from the response as the doc ID for step 2.

### Step 2. Append the log line

```bash
porteden docs edit <DOC_ID> --append "[09:30:00Z] deploy | production | v2.4.1 released | success"
```

Each `--append` adds text at the end of the document, preserving all previous entries.

**Multiple lines in one call:**

```bash
porteden docs edit <DOC_ID> --append "[09:30:00Z] deploy | production | v2.4.1 released | success
[09:31:12Z] healthcheck | production | all endpoints healthy | success"
```

## Log format examples

Use a consistent line format. Recommended patterns:

**Timestamped event:** `[HH:MM:SSZ] event | source | details | status`

**Audit entry:** `[HH:MM:SSZ] actor | action | resource | result`

**Error line:** `[HH:MM:SSZ] ERROR | service | message`

**Task result:** `[HH:MM:SSZ] task | agent | input → output | duration`

The date is already in the document name — log lines only need the time component.

## Reading logs

Read today's log:

```bash
porteden docs read <DOC_ID>
```

List all log documents in the folder:

```bash
porteden drive files --folder $PE_LOG_FOLDER -jc
```

Read a specific day's log:

```bash
porteden drive files --name "2025-01-10" --folder $PE_LOG_FOLDER --mime-type application/vnd.google-apps.document -jc
```

Then read by its ID:

```bash
porteden docs read <DOC_ID>
```

## Best practices

1. **Always use `--append`** — never overwrite log docs. Append-only preserves the full audit trail.
2. **Use ISO 8601 date for doc names** (`YYYY-MM-DD`) — ensures chronological sort and unique daily docs.
3. **Include only the time in log lines** — the date is in the document name, no need to repeat it.
4. **Batch multiple log lines in one `--append`** — separate lines with `\n` to reduce API calls.
5. **Use a consistent delimiter** — pipe `|` keeps fields scannable. Avoid commas in free-text fields.
6. **Search before creating** — always check if today's doc exists before creating a new one to avoid duplicates.
7. **Use `-jc` on drive/read calls** — compact JSON output minimizes tokens for AI agents.

## Notes

- Credentials persist in the system keyring after login. No repeated auth needed.
- Set `PE_PROFILE=work` to avoid repeating `--profile`.
- `-jc` is shorthand for `--json --compact`: strips noise, limits fields, reduces tokens for AI agents.
- **File IDs are always provider-prefixed** (e.g., `google:1BxiMVs0XRA5...`). Pass them as-is.
- `porteden docs read` returns plain text by default.
- `--append` adds text at the end of the document. Each call appends — it does not replace.
- `accessInfo` in responses describes active token restrictions.
- `PE_LOG_FOLDER` is the only env var specific to this skill. Store it alongside `PE_API_KEY`.
- Environment variables: `PE_API_KEY`, `PE_PROFILE`, `PE_LOG_FOLDER`, `PE_FORMAT`, `PE_COLOR`, `PE_VERBOSE`.
