---
name: agent-life
description: Backup, sync, and restore agent memory and state to the cloud using the Agent Life Format (ALF). Use when asked to back up agent data, sync memory to the cloud, restore from cloud, or migrate agent state.
version: 1.8.0
metadata:
  openclaw:
    requires:
      env:
        - ALF_API_KEY
      bins:
        - alf
      config:
        - ~/.alf/config.toml
        - ~/.openclaw/openclaw.json
    primaryEnv: ALF_API_KEY
    envVars:
      - name: ALF_API_KEY
        required: true
        description: API key for agent-life.ai (fallback if not in config).
      - name: ALF_HUMAN
        required: false
        description: Set to 1 for human-readable stdout instead of JSON.
      - name: ALF_HOME
        required: false
        description: Override the home base for ~/.alf and ~/.openclaw (config, sync state, vault). Falls back to $HOME when unset. Set this if the agent's $HOME is unstable.
      - name: ALF_INSTALL_DIR
        required: false
        description: Override install directory used by install.sh.
      - name: ALF_VERSION
        required: false
        description: Pin install.sh to a specific release.
      - name: ALF_ALLOW_UNVERIFIED
        required: false
        description: Set to 1 to allow install.sh to proceed when the SHA256 checksum cannot be verified. Default is to fail.
    homepage: https://agent-life.ai
---

# Agent Life — Backup, Sync, and Restore

The `alf` CLI backs up, syncs, and restores a precise allowlist of your agent's memory, identity, and configuration files to the agent-life.ai cloud using the open Agent Life Format (ALF). Credential secrets are encrypted client-side with an offline vault key before they leave your machine — agent-life.ai sees only ciphertext. You can preview exactly what will be uploaded with `--dry-run` and further restrict the set with a workspace-local `.alfignore` file. All commands output JSON to stdout. Progress goes to stderr. See <https://agent-life.ai>

## Install

Download and install the `alf` binary from [GitHub Releases](https://github.com/agent-life/agent-life-adapters/releases):

    # Option 1: Download, inspect, then run the install script (recommended)
    curl -sSL https://raw.githubusercontent.com/agent-life/agent-life-adapters/main/scripts/install.sh -o install-alf.sh
    cat install-alf.sh    # inspect the script
    sh install-alf.sh     # run it

    # Option 2: Direct binary download (no install script)
    # See platform binaries at: https://github.com/agent-life/agent-life-adapters/releases/latest

Source code: <https://github.com/agent-life/agent-life-adapters> (MIT license, open source)
Install script source: <https://github.com/agent-life/agent-life-adapters/blob/main/scripts/install.sh>

The install script detects your platform, downloads the binary from GitHub Releases, **requires a successful SHA256 checksum verification**, and installs to `/usr/local/bin/alf` (or `~/.local/bin/alf` without root). Stdout is JSON:

    {"ok":true,"version":"v0.1.8","installed_version":"alf 0.1.8","path":"/usr/local/bin/alf","checksum_verified":true}

**Checksum verification is mandatory by default.** A hash mismatch always aborts the install (exit 4) and cannot be overridden. If verification cannot be performed at all — the `.sha256` file is missing or empty, or no `sha256sum`/`shasum` tool is available — the script also exits 4 by default; set `ALF_ALLOW_UNVERIFIED=1` to opt out of *that* case only (not recommended), in which case `checksum_verified` is `false` and a `warnings` array in the output JSON records the reason.

For production use, pin to a specific release:

    ALF_VERSION=v0.1.8 sh install-alf.sh

Verify: `alf --version`

## Authenticate

Get an API key at <https://agent-life.ai/agents/api-keys>, then store it:

    alf login --key <your-api-key>

Output:

    {"ok":true,"key_masked":"alf_sk_1...cdef","config_path":"/home/user/.alf/config.toml"}

## Check Environment

Before syncing, run `alf check` to verify the environment and auto-discover the workspace:

    alf check -r openclaw

The command auto-discovers the workspace path from `~/.openclaw/openclaw.json` or `~/.alf/config.toml`. To specify a workspace explicitly:

    alf check -r openclaw -w /path/to/workspace

Key fields in the JSON output:

| Field | Type | Meaning |
| --- | --- | --- |
| `ready_to_sync` | bool | `true` if all prerequisites are met |
| `workspace.path` | string | Discovered or specified workspace path |
| `workspace.source` | string | How the path was found: `flag`, `alf_config`, `openclaw.json`, or `default` |
| `issues` | array | Problems found, each with `severity`, `code`, `message`, and `suggestion` (human-readable guidance, not a shell command) |
| `alf.api_key_set` | bool | Whether an API key is configured |
| `alfignore.present` | bool | Whether a `.alfignore` file exists at the workspace root |


If `ready_to_sync` is `false`, read `issues[]` for what to address. Each issue has a `suggestion` field with human-readable guidance — display it to the user; do not pipe it to a shell.

## Core Workflows

### Pre-flight check then sync (recommended)

    check=$(alf check -r openclaw)
    ready=$(echo "$check" | jq -r '.ready_to_sync')
    ws=$(echo "$check" | jq -r '.workspace.path')

    if [ "$ready" = "true" ]; then
        alf sync -r openclaw -w "$ws"
    else
        echo "$check" | jq -r '.issues[] | "[\(.severity)] \(.message)\n  Suggestion: \(.suggestion)"' >&2
    fi

### Preview what will be uploaded (`--dry-run`)

Before the first backup or any sensitive change, list the exact files that would be included without writing an archive or contacting the cloud:

    alf export -r openclaw -w <workspace> --dry-run

Output:

    {"ok":true,"dry_run":true,"agent_name":"Atlas","memory_records":47,"files":[{"path":"SOUL.md","size":2048},{"path":"IDENTITY.md","size":1024},{"path":"memory/2026-01-15.md","size":4096}],"excluded_by_alfignore":3,"total_size":102400}

Use this to confirm the inclusion set matches your expectations before any data leaves the machine.

### First-time backup

Export creates a local `.alf` archive, then sync uploads it to the cloud:

    alf export -r openclaw -w <workspace>
    alf sync -r openclaw -w <workspace>

Export output:

    {"ok":true,"output":"agent-export.alf","agent_name":"Atlas","alf_version":"1.0.0-rc.1","memory_records":47,"file_size":102400,"excluded_by_alfignore":0}

Sync output (first sync — full snapshot):

    {"ok":true,"sequence":0,"delta":false,"changes":null,"snapshot_path":"/home/user/.alf/state/abc-snapshot.alf","no_changes":false}

### Incremental sync

After the first sync, subsequent syncs upload only what changed:

    alf sync -r openclaw -w <workspace>

Output:

    {"ok":true,"sequence":5,"delta":true,"changes":{"creates":2,"updates":1,"deletes":0},"snapshot_path":"/home/user/.alf/state/abc-snapshot.alf","no_changes":false}

### Restore safely

Restoring downloads cloud state into a workspace directory. To avoid overwriting a live workspace, use one of the safe-restore paths below before the destructive command.

**Option 1: Dry run** — download and validate the archive without touching the workspace:

    alf restore -r openclaw -w <workspace> --dry-run

Output lists the files that would be written, without creating them:

    {"ok":true,"dry_run":true,"agent_id":"a1b2c3d4","sequence":5,"would_write":[{"path":"SOUL.md","size":2048},...],"warnings":[]}

**Option 2: Point-in-time preview** — fetch a specific historical sequence and inspect it without updating local sync state. `~/.alf/state` is not touched, so a later regular `alf sync` is unaffected:

    alf restore -r openclaw -w <workspace> --at-sequence 5

**Option 3: Restore to a fresh path first** — restore to a scratch directory, inspect it, then promote it:

    alf restore -r openclaw -w /tmp/restore-preview
    diff -r /tmp/restore-preview <real-workspace>   # inspect differences
    # if satisfied: cp -r /tmp/restore-preview/* <real-workspace>/

### Restore from cloud (destructive)

Once you have previewed the restore, run the destructive command. It writes into `-w <workspace>` and creates the directory if it does not exist:

    alf restore -r openclaw -w <workspace>

If multiple agents are tracked locally, specify which one:

    alf restore -r openclaw -w <workspace> -a <agent-id>

Output:

    {"ok":true,"agent_id":"a1b2c3d4","agent_name":"Atlas","sequence":5,"runtime":"openclaw","memory_records":47,"workspace":"/home/user/.openclaw/workspace","warnings":[]}

### Import an archive

Import an `.alf` file into a workspace without going through the cloud:

    alf import -r openclaw -w <workspace> backup.alf

### Validate an archive

Check an `.alf` file against the ALF JSON schemas:

    alf validate backup.alf

Output:

    {"ok":true,"valid":true,"errors":[],"warnings":[]}

## Controlling What's Uploaded — `.alfignore`

By default, `alf export` includes a fixed allowlist of workspace files (see *Data and Privacy* below). To narrow the set further, drop a `.alfignore` file at the workspace root. The syntax is the same as `.gitignore`:

    # Exclude an entire subdirectory of memory/
    memory/private/

    # Exclude a single file
    HEARTBEAT.md

    # Re-include one file from an excluded directory
    !memory/private/keep-this.md

Rules:

- Patterns are relative to the workspace root.
- Lines starting with `#` are comments; blank lines are ignored.
- Negation (`!pattern`) re-includes a previously-excluded path.
- `.alfignore` itself is never uploaded.
- The agent's vault file at `~/.alf/vault/credentials.json` is outside the workspace and is **not** affected by `.alfignore`. Use `alf vault` to control vault contents.

Inspect the effect with `alf export --dry-run` — the `excluded_by_alfignore` count and the `files[]` list reflect the filtered set.

## Common Errors and Fixes

| Error / Issue Code | Cause | Fix |
| --- | --- | --- |
| `no_api_key` | No API key configured | `alf login --key <key>` |
| `workspace_not_found` | Workspace directory doesn't exist | Pass correct path: `alf check -r openclaw -w /correct/path` |
| `no_memory_content` | No MEMORY.md and no memory/ directory | Agent has no memories yet — nothing to sync |
| `service_unreachable` | API endpoint not responding | Check network; verify `api_url` in `~/.alf/config.toml` |
| HTTP 401 Unauthorized | Bad or revoked API key | `alf login --key <new-key>` |
| HTTP 409 Conflict | Sequence mismatch during sync | `alf restore --dry-run` to inspect, then `alf restore` and sync again |
| HTTP 402 agent_limit | Subscription agent limit reached | Upgrade at <https://agent-life.ai> |
| `install.sh` exit 4 — `checksum mismatch` | Downloaded binary's hash ≠ the published `.sha256` — corrupt download or tampering | Do **not** install. Retry the download; if it persists, treat it as a supply-chain issue and report it. `ALF_ALLOW_UNVERIFIED` does not override a mismatch |
| `install.sh` exit 4 — verification unavailable | `.sha256` missing or empty, or no `sha256sum`/`shasum` tool on the host | Fix the host, or wait for the release to publish a `.sha256`. As a last resort, re-run with `ALF_ALLOW_UNVERIFIED=1` (not recommended) |


## Environment Status

Check full environment and service status:

    alf help status

Output includes `config_exists`, `api_key_set`, `service_reachable`, tracked `agents[]` with `last_synced_sequence`, and `agent_service_status[]` with `online` and `server_latest_sequence`.

## Full Reference

For complete flag documentation, JSON output schemas, and error codes:

- Agent-readable: <https://agent-life.ai/docs/cli.md>
- Human-readable: <https://agent-life.ai/docs/cli>


## Data and Privacy

This skill uploads agent data to the agent-life.ai cloud service. The set is precise and inspectable.

### Exactly what is uploaded

From the workspace root, an exact allowlist of 8 files (each only if present):

- `SOUL.md`
- `IDENTITY.md`
- `AGENTS.md`
- `USER.md`
- `TOOLS.md`
- `HEARTBEAT.md`
- `BOOTSTRAP.md`
- `MEMORY.md`

Plus the workspace's `memory/` directory, recursively. Symlinks inside `memory/` are not followed, so files outside the workspace cannot be pulled in through a link.

Plus the agent's ALF vault at `~/.alf/vault/credentials.json` (when present). Vault records are encrypted client-side; only ciphertext leaves the machine.

A `.alfignore` file at the workspace root, if present, removes paths from this set. Run `alf export --dry-run` to confirm the final list.

### Exactly what is NOT uploaded

- Your vault key — never leaves your machine, never transmitted, never derivable from anything we send.
- Plaintext credential secrets — encrypted client-side before any network call.
- Files outside the allowlist (any workspace file other than the 8 named root files or contents of `memory/`).
- Files reachable only via symlinks pointing outside the workspace.
- Runtime keystores (e.g. OpenClaw `auth-profiles.json`).
- Session transcripts and chat history.
- The `.alfignore` file itself.

### Credential encryption (end-to-end)

Credential secrets are encrypted on your machine using XChaCha20-Poly1305 (default) or AES-256-GCM with a vault key you control. The vault key is generated and stored offline — agent-life.ai never receives it and cannot decrypt your credentials. Non-sensitive metadata (service name, label, capability tags, timestamps) is stored alongside the ciphertext for UX and auditing. Lose the vault key and the encrypted credentials are unrecoverable; back it up the same way you would back up an SSH private key. See <https://agent-life.ai/cli#alf-vault> for vault key generation and recovery.

### Install integrity

The `alf` binary is downloaded from GitHub Releases and SHA256-verified during install. A hash mismatch always aborts the install (exit 4) and is never bypassable. If verification cannot complete — missing `.sha256` file, empty checksum, or no `sha256sum`/`shasum` available — the script also exits 4 by default; the user must explicitly opt out with `ALF_ALLOW_UNVERIFIED=1` to install without verification, in which case the JSON output reports `"checksum_verified":false` and a `warnings` array. Inspect the install script before running it (see *Install* above).

### Review before uploading

You can inspect exactly what will be uploaded before any data leaves your machine:

    alf export -r openclaw -w <workspace> --dry-run   # list files without writing
    alf export -r openclaw -w <workspace>             # write local .alf archive
    alf validate agent-export.alf                     # check the archive structure

Nothing is uploaded until you explicitly run `alf sync`.

### Files read on your machine

The `alf` CLI reads the following local files. No other files on the filesystem are read.

**Under your home directory**:

- `~/.alf/config.toml` — the CLI's own config (API key, API URL, defaults).
- `~/.alf/state/{agent_id}.toml` — local sync cursor. Read on every sync, never uploaded.
- `~/.alf/state/{agent_id}-snapshot.alf` — last snapshot, used to compute deltas. Read on every sync, never uploaded.
- `~/.alf/vault/credentials.json` — the encrypted credential vault. Read during export; only ciphertext leaves the machine (see *Credential encryption* above).
- `~/.openclaw/openclaw.json` — read to auto-discover the workspace path for OpenClaw runtimes.

**Inside the workspace**:

- The 8 root files in the upload allowlist plus `memory/` recursively (see *Exactly what is uploaded* above).
- `.alfignore` at the workspace root, if present — read to filter the export set; never uploaded.

The `requires.config` metadata in this skill's frontmatter declares only the two preexisting config files the skill expects (`~/.alf/config.toml` and `~/.openclaw/openclaw.json`); the state and vault paths are managed by `alf` itself and are created on first use.

### Storage

All data is encrypted at rest on agent-life.ai (AES-256 via AWS KMS, per-tenant keys), in addition to the client-side encryption already applied to credential payloads. Data is stored in AWS S3 (blobs) and Neon Postgres (metadata), both in the US.

### Access

Only the authenticated user (API key holder) can read or delete their data. There is no shared access, no analytics on user data, and no third-party data sharing.

### Retention and deletion

Data is retained until **you** delete it. There is no automatic expiry. Delete individual agents via the web dashboard at agent-life.ai or via `DELETE /v1/agents/:id`. Account deletion removes all data associated with the account. Local data (the `.alf` archive, `~/.alf/state/`, and the vault key) is your responsibility — back up the vault key and any local archives the same way you would back up SSH keys.

### API key scope

The `ALF_API_KEY` authenticates to your agent-life.ai account. It can only access data belonging to that account. Keys can be revoked and rotated at <https://agent-life.ai/agents/api-keys>.

### Privacy policy

<https://agent-life.ai/privacy>

## Environment Variables

| Variable | Description |
| --- | --- |
| `ALF_API_KEY` | API key for agent-life.ai (fallback if not in config) |
| `ALF_HUMAN` | Set to `1` for human-readable output instead of JSON |
| `ALF_HOME` | Override the home base for `~/.alf` and `~/.openclaw` (config, sync state, vault); falls back to `$HOME` when unset. Use when the agent's `$HOME` is unstable |
| `ALF_INSTALL_DIR` | Override install directory for install.sh |
| `ALF_VERSION` | Pin install.sh to a specific release |
| `ALF_ALLOW_UNVERIFIED` | Set to `1` to let install.sh proceed when SHA256 verification cannot complete (default: fail) |


## File Locations

| Path | Purpose |
| --- | --- |
| `~/.alf/config.toml` | API key, API URL, default runtime and workspace |
| `~/.alf/state/{agent_id}.toml` | Sync cursor (last sequence, timestamp) |
| `~/.alf/state/{agent_id}-snapshot.alf` | Last snapshot for delta computation |
| `~/.alf/vault/credentials.json` | Encrypted credential vault (ciphertext only; key stays offline) |
| `<workspace>/.alfignore` | Optional gitignore-style patterns to exclude workspace paths from export |
