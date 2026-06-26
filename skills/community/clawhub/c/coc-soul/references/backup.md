# `coc-soul backup` — soul backup and restore

## First-time

- `backup init` — register the agent on SoulRegistry (if not yet registered), run a first **full** backup, write `~/.coc-backup/latest-recovery.json` with the decryption material + manifest CID.
- `backup register` — register on-chain only, do not run a backup.

## Periodic

- `backup create` — incremental (default); `--full` forces a full backup regardless of chain length.
  - `backup.autoBackup: true` + `backup.autoBackupIntervalMs` runs this on a timer inside the OpenClaw plugin.
- `backup.backupOnSessionEnd: true` + a `session_end` hook from OpenClaw also triggers `backup create` when the agent's session closes.

### Output: `backup create` recovery summary (1.2.6+)

Every successful `backup create` prints two blocks. The first is the receipt; the second is what the user needs to restore the backup later — relay it verbatim to the user (don't swallow it):

```
Backup complete (full):
  manifest:   <cid>
  files:      <n>
  bytes:      <n>
  merkleRoot: 0x...
  txHash:     0x...           # only present if anchored on-chain

Recovery info — keep this safe to restore on another host:
  recovery package: <sourceDir>/.coc-backup/latest-recovery.json
  encryption mode:  none | privateKey | password
  signing key file: <path>    # mode 0600 — copy off-host securely
  signer address:   0x...

To restore on another host (always restore to /tmp first, verify, then promote):
  openclaw coc-soul backup restore --manifest-cid <cid> \
    --target-dir /tmp/openclaw-restore-test [ --password '<pw>' ]

  (if you also have <path>/latest-recovery.json on the target host:)
  openclaw coc-soul backup restore --latest-local --target-dir /tmp/openclaw-restore-test [ --password '<pw>' ]
```

The `--password` clause appears only when `encryption mode = password`. In `privateKey` mode, the operator must instead make sure the right key is loaded on the target host (either by copying the keystore file or by setting `backup.privateKey` in target's config).

The same fields are persisted in `<sourceDir>/.coc-backup/latest-recovery.json` (a small JSON written atomically after every backup) so the info survives even if the operator missed the terminal output:

```jsonc
{
  "version": 1,
  "agentId": "0x...",
  "latestManifestCid": "bafy...",
  "anchoredAt": 1777180566,
  "txHash": "0x...",
  "dataMerkleRoot": "0x...",
  "backupType": "full" | "incremental",
  "encryptionMode": "none" | "privateKey" | "password",
  "requiresPassword": false | true,
  "recommendedRestoreCommand": "openclaw coc-soul backup restore --latest-local --target-dir /tmp/openclaw-restore-test ..."
}
```

Treat both `latest-recovery.json` AND the signing-key file as a pair — back them up together (the manifest CID is also visible on-chain via the SoulRegistry contract, so even losing `latest-recovery.json` is recoverable from `backup find-recoverable --on-chain`, but losing the key means the encrypted payload is permanently unreadable).

## Inspect

- `backup status` — concise: chain registration state, last backup time, IPFS reachability
- `backup doctor` — structured diagnosis with actionable `recommended actions`. Use when something feels off.
- `backup list` / `backup history` — local archive table

## Restore (safety-first)

**Default: restore to `/tmp` first, verify, then promote.** Never overwrite a production directory with an unverified backup.

### Pre-restore inspection

If a local recovery package exists, read it first to know which mode + key the backup was written with:

```bash
cat ~/.openclaw/.coc-backup/latest-recovery.json
```

Capture:
- `latestManifestCid` — what to restore
- `encryptionMode` — `privateKey` | `password` | `none`
- `requiresPassword` — whether `--password` is required

### Restore commands (always to a temp dir first)

From local package:

```bash
openclaw coc-soul backup restore \
  --package /path/to/latest-recovery.json \
  --target-dir /tmp/openclaw-restore-test
```

From the latest local package (most common):

```bash
openclaw coc-soul backup restore \
  --latest-local \
  --target-dir /tmp/openclaw-restore-test
```

From a manifest CID:

```bash
openclaw coc-soul backup restore \
  --manifest-cid <CID> \
  --target-dir /tmp/openclaw-restore-test
```

### encryptionMode handling

- `encryptionMode: "password"` (or `requiresPassword: true`) → add `--password '<your-password>'`
- `encryptionMode: "privateKey"` → **do NOT pass `--password`**; ensure the right `backup.privateKey` / keystore key is loaded
- `encryptionMode: "none"` → no extra flag needed

Mismatched mode is the #1 reason `Unsupported state or unable to authenticate data` shows up. Triage that error as mode/key mismatch before suspecting tampering.

### Verify before promoting

Success criteria:
- exit code `0`
- output contains `merkleVerified: true`

If verification passes, **only then** confirm with the user before copying / moving the restored tree onto the production path.

### Cross-host restore: directory-mismatch handling

A backup made on a host where `$HOME=/home/node` will contain absolute paths like `/home/node/.openclaw/...`. Restoring on a host with `$HOME=/home/baominghao` puts those paths in the agent state where they don't exist. Rather than blindly string-replacing every occurrence (which silently corrupts SQLite binaries and rewrites historical chat content), the operator decides per-restore.

**Step 1 — detect the mismatch.** After restore-to-temp completes, scan the restored tree:

```bash
# Look for paths that don't match the current $HOME
grep -lrE '/home/[a-zA-Z_-]+/\.openclaw' /tmp/openclaw-restore-test 2>/dev/null \
  | head -20
```

If any hit is from a path that's **not** the current `$HOME`, you have a cross-host restore.

**Step 2 — explain to the user, get a decision.** Present three options:

1. **Read-only inspect** — leave paths as-is, mount the restored tree only for inspection. Useful when you just want to recover a specific file or audit history without resuming the agent.
2. **Smart rebase** (recommended for resuming the agent) — rewrite **only** runtime-config paths, leave historical content intact. See the three-class table below.
3. **Full literal overwrite** — what happens if you don't intervene; almost always wrong (corrupts history, can break SQLite).

**Step 3 — apply smart rebase.** Three classes of content, three different policies:

| Class | What it is | Examples | Policy |
|---|---|---|---|
| **A. Runtime config (paths)** | Settings the runtime reads to find files on disk now | `openclaw.json` `agentDir` / `paths.*`, `models.json` paths, `device.json`, `latest-recovery.json` `targetDir` / `sourceDir`, `context-snapshot.json` cwd refs | **Rewrite** old `$HOME` → new `$HOME`. Done structurally (JSON parse → field edit → re-emit), never via byte-level `sed` |
| **B. Historical content** | Records of past events that **were** at those paths when written | `agents/*/sessions/*.jsonl` (tool calls + outputs), `memory/main.sqlite` `observations.{narrative,facts,files_read,files_modified}`, `semantic-snapshot.json` summaries | **Leave intact**. Rewriting fakes history. claw-mem runtime never blindly opens those paths — it just searches FTS text. |
| **C. Host-local policy (CRITICAL — see auth section below)** | Settings that belong to **this** host's operator, not the agent | `gateway.auth.*`, `gateway.bind`, `gateway.port`, `plugins.allow`, host-specific provider keys in `models.json` | **Preserve target host's existing values** — don't overlay the backup's. The new host's operator already configured these for the new environment. |

The rebase routine should:
1. Parse target file as JSON / structured (not byte-level `sed`)
2. Edit only A-class fields
3. For C-class fields in `openclaw.json`, **merge** rather than overwrite: keep the target host's existing `gateway.auth.*` / `gateway.bind` / `plugins.allow` exactly; only adopt the backup's agent-portable fields
4. Skip B-class files entirely
5. Write a `rebase-report.json` next to the restored tree so operators can audit what changed

**Step 4 — auth: re-confirm before launching the gateway.**

After rebase, dump the effective `gateway.auth` and use the matching TUI invocation:

```bash
jq '.gateway.auth' ~/.openclaw/openclaw.json
```

| `auth.mode` | TUI invocation |
|---|---|
| `"token"` | `openclaw tui --token "$(jq -r .gateway.auth.token ~/.openclaw/openclaw.json)"` |
| `"password"` | `openclaw tui --password '<password>'` |
| `"trusted-proxy"` | `openclaw tui --password '<password>'` (if header-based auth fronts the gateway, trust the proxy header in dev; otherwise pass `--password`) |
| `"none"` | `openclaw tui` |

**Common pitfall**: post-restore, `openclaw tui --token "$(jq -r .gateway.auth.token openclaw.json)"` returns the literal string `null` when the active auth mode no longer has a `.token` field (e.g. `mode` is now `password` or `trusted-proxy`). The TUI dutifully sends `null` and the gateway rejects with **1008**. Always re-read `auth.mode` after restore and pick the matching flag.

### Auth-mode preservation rule (must read before any production restore)

The most common production-breaking restore mistake: backup contains `gateway.auth.mode = "token"` with a valid token from the source host; target host has been carefully configured with `mode = "trusted-proxy"` or `"password"`. A literal-overwrite restore replaces target's auth, then the operator on target can't log in anymore — and **the backup's token is for a different gateway instance, useless on this host**.

Rule: **`gateway.auth` is a property of the host, not of the agent.** It does not get restored. The smart-rebase path explicitly preserves the target host's `gateway.auth.*` block. If you must do a literal overwrite (e.g. recovering on a fresh host with no existing config), regenerate auth before starting the gateway:

```bash
openclaw gateway init --auth password
# or whatever mode the new host should use
```

### Discover what this key can restore

```bash
openclaw coc-soul backup find-recoverable --json           # local index
openclaw coc-soul backup find-recoverable --on-chain --json # walk the chain
```

## Prune

`backup prune` only touches **local archive index entries**, not IPFS pins.

```bash
openclaw coc-soul backup prune --older-than 30 --keep-latest 1 --dry-run
openclaw coc-soul backup prune --older-than 30 --keep-latest 1
```

## What gets backed up — file patterns (1.2.9)

The backup walks `~/.openclaw/` (or the configured `backup.sourceDir`) and captures files that match a built-in classifier. Patterns explicitly support **both** the legacy root-level layout and the current `workspace/`-prefixed layout that OpenClaw uses, so the backup picks up identity / memory files no matter which version of OpenClaw wrote them.

### Identity (markdowns; root **or** `workspace/`; not encrypted)
- `IDENTITY.md` — agent identity declaration (where the agent's name lives)
- `SOUL.md` — soul configuration
- `BOOTSTRAP.md` — bootstrap / setup instructions (1.2.9+)

### Memory (markdowns; root **or** `workspace/`; not encrypted)
- `MEMORY.md`
- `USER.md`
- `RECOVERY_CONTEXT.md` (regenerated on restore)
- everything under `memory/*.md` **or** `workspace/memory/*.md` (1.2.9+) — daily / per-topic notes (`workspace/memory/2026-04-27.md`, `workspace/memory/topic-foo.md`, etc.)

### Workspace (markdowns + state; root **or** `workspace/`; not encrypted)
- `AGENTS.md`
- `TOOLS.md` — tools manifest (1.2.9+)
- `HEARTBEAT.md` — soul's own heartbeat file (1.2.9+; soul writes it, soul backs it up)
- `workspace-state.json` (root location, legacy)
- `workspace/.openclaw/workspace-state.json` (current OpenClaw layout, 1.2.9+)

### Identity / config (fixed paths)
- `identity/device.json` (config, **encrypted**)
- `identity/device-auth.json` (config, **encrypted**, 1.2.9+ — paired with device.json for cross-device auth)
- `auth.json` (config, **encrypted**)
- `openclaw.json` (config, **encrypted**)
- `agents/<id>/agent/models.json` (config, **encrypted**, 1.2.9+ — holds literal LLM API keys after the 1.2.6 persistence change; **MUST** stay encrypted)
- `exec-approvals.json` (config, **encrypted**, 1.2.9+ — Bash / tool approval rules)
- `plugins/*/openclaw.plugin.json` (config, not encrypted)
- `credentials/*` (config, **encrypted**)

### Chat (not encrypted)
- `agents/*/sessions/*.jsonl`
- `agents/*/sessions/sessions.json`

### Database (encrypted)
- `memory/*.sqlite` (and SQLite WAL/SHM siblings)
- `memory/lancedb/*`

### Metadata
- `.coc-backup/context-snapshot.json` (workspace, auto-generated)
- `.coc-backup/semantic-snapshot.json` (memory, auto-generated)

### Walker descends into hidden dirs (`.`-prefixed) — allow-list

Walker skips `.`-prefixed directories by default to avoid pulling `.git/`, `.cache/`, etc. Three names are allow-listed: `.claude` (historical), `.coc-backup` (snapshot metadata), `.openclaw` (workspace state — added 1.2.9 to reach `workspace/.openclaw/workspace-state.json`). To extend the allow-list, edit `scanFiles()` in `src/backup/change-detector.ts`.

## What is intentionally excluded — denylist (1.2.10+)

Even when files are in a backed-up directory, the walker / classifier explicitly excludes the following to avoid wasted IO, host-cross-contamination, and circular references:

### Host-local secrets — must NEVER travel between hosts

| File | Why |
|---|---|
| `agents/<id>/agent/models.json` | LLM provider config; post-1.2.6 holds literal API tokens (`ANTHROPIC_AUTH_TOKEN` etc.). Each host has its own provider keys; copying source's keys to target is at best a leak, at worst breaks the target host's auth. Restore the agent, then re-configure provider on target via `openclaw infer model auth login`. |
| `agents/<id>/agent/auth-profiles.json` | OAuth profiles. Same reason — host-local credential state. |

### Operator audit copies — file-name patterns skipped at walker level

Skipped regardless of which directory they appear in:
- `*.bak`, `*.bak.<n>` — operator's manual backups
- `*.pre-<label>` — operator's pre-change snapshots (`openclaw.json.pre-allowlist`, `models.json.pre-llm-config`)
- `*.rejected.<iso-ts>` — config writes the gateway rejected (`openclaw.json.rejected.2026-04-23T09-35-42-752Z`)
- `*.last-good` — last known-good config marker
- `stale-*-backup-*.tar.gz` — operator's self-archives

### Install / restore audit dirs — pruned at walker level

Walker never enters these directories:
- `.git/` — git-managed history; backed up via git itself, not via soul
- `node_modules/` — re-installed per host via `openclaw plugins install`
- `.openclaw-install-backups/` — `openclaw plugins install` rotation copies
- `.restore-overwrite-backup-<ts>/` — pre-restore audit copy of openclaw home (left behind by previous restore-overwrite operations)

### Circular-reference state

| File | Why |
|---|---|
| `.coc-backup/state.json` | Holds `lastManifestCid` + `incrementalCount` — the **head of the backup chain itself**. Including it in a new backup creates a circular reference: the chain head would point at a state that doesn't exist yet. The chain head is restored by reading the manifest hierarchy on the target host, not by copying the source's pointer. |

### Already excluded by virtue of not matching FILE_RULES

These are skipped because nothing in the whitelist matches them — they're listed here so the design intent is explicit:
- `extensions/**` — plugin install dir; reinstalled per host
- `flows/registry.sqlite`, `tasks/runs.sqlite` (+ WAL/SHM siblings) — operational state, not portable
- `logs/**`, `canvas/**`, `update-check.json` — regenerable
- `*.sqlite-wal`, `*.sqlite-shm` — SQLite write-ahead-log artifacts; the main `.sqlite` carries everything needed
- `agents/*/sessions/*.jsonl.reset.<ts>` — operator-side session-reset markers
- `workspace/.git/**` (also denylisted explicitly above for defense in depth)

### Adding to the denylist

If you find another file that's leaking into manifests it shouldn't, edit:
- **dir-name skip**: `SKIP_DIRS_BY_NAME` or `SKIP_DIR_NAME_PATTERNS` in `src/backup/change-detector.ts`
- **file-name skip**: `SKIP_FILE_NAME_PATTERNS`
- **specific path skip**: `SKIP_FILE_RELATIVE_PATHS`
- pair with a regression test in `test/backup-suite/change-detector-extended.test.ts`

### Files outside this whitelist are NOT backed up

If you put important state in `~/.openclaw/<custom-dir>/` and the path doesn't match any pattern above, it will be silently skipped — extend the pattern set in `src/backup/change-detector.ts` and bump soul minor version if you need a new shape covered. **Always pair a pattern addition with a regression test** in `test/backup-suite/change-detector-extended.test.ts`.

### Upgrade notes

| From | What to do after upgrade |
|---|---|
| **pre-1.2.7** (no workspace/ prefix support) | Run `openclaw coc-soul backup create --full` once. Verify `workspace/IDENTITY.md` shows up in `backup list --json` file count + restore-to-`/tmp` smoke. |
| **1.2.7 / 1.2.8** | Run `backup create --full` once. New 1.2.9 patterns (`TOOLS.md`, `HEARTBEAT.md`, `BOOTSTRAP.md`, `workspace/memory/*.md`, `workspace/.openclaw/workspace-state.json`, `identity/device-auth.json`, `agents/<id>/agent/models.json`, `exec-approvals.json`) will be added to the manifest. |

## Categories & semantic snapshot

`backup.categories.*` controls what gets bundled:

- `identity` — DID + keys
- `config` — OpenClaw / claw-mem config
- `memory` — SQLite memory DB
- `chat` — conversation history
- `workspace` — agent's working dir
- `database` — other DBs

`backup.semanticSnapshot` controls the compressed "agent context" snapshot included with each backup:

- `enabled` (default `true`) — pack a token-budgeted summary of memory
- `tokenBudget` (default 8000)
- `maxObservations` / `maxSummaries`

## Encryption

- `backup.encryptMemory: true` + `backup.encryptionPassword` — AES-GCM encrypt memory before IPFS upload
- Without encryption, backups are still integrity-checked via Merkle root but readable by anyone who fetches the CID

## Resurrection prep

- `backup configure-resurrection --resurrection-key-hash <bytes32> --max-offline-duration <seconds>` — set the "trigger" for an automatic resurrection request
- `backup heartbeat` — send a heartbeat so automatic resurrection doesn't fire

After both are set, verify with `backup doctor --json` — `resurrection.configured` must be `true`.

## CID + key disambiguation

| Term | What it is | Where it shows up |
|---|---|---|
| `latestManifestCid` | Latest restore point | `latest-recovery.json`, `backup status` |
| older full CID | Historical baseline restore point | `backup history` |
| identity CID / hash | Identity-content hash from registration | DID write commands — **not** a restore point |

Private keys (owner / resurrection / guardian) are **never** chat-safe. Don't transmit even split / encrypted fragments via chat.

## Failure-mode triage

| Symptom | Likely cause | Action |
|---|---|---|
| `Unsupported state or unable to authenticate data` | encryption mode / key mismatch | Re-read `latest-recovery.json` `encryptionMode` and use the matching `--password` (or none) |
| `429 rate limit exceeded` | IPFS gateway rate-limited | Retry with exponential backoff until `merkleVerified: true` |
| restore unavailable / blocked | chain not registered or no manifest | Run `backup doctor --json`; fix `chain.registered` first |
| `[gateway] unauthorized (1008)` | gateway auth / proxy mode wrong | Fix gateway auth (token / OAuth / proxy) before scheduled `heartbeat` |
| `[gateway] unauthorized (1008)` **right after restore** | restore overwrote `gateway.auth.mode` (was `token`, now `trusted-proxy` / `password`); old TUI command sends literal `null` token | `jq '.gateway.auth.mode' ~/.openclaw/openclaw.json` to see active mode; switch TUI invocation per the auth-mode table above. If smart-rebase wasn't used, restore target host's `gateway.auth.*` from the pre-restore backup at `~/.openclaw/.restore-overwrite-backup-*/openclaw.json` |
| Cross-host restored agent has stale paths in chat / observations | literal overwrite was used, OR smart-rebase ran on B-class history files (it shouldn't) | Roll those files back from `.restore-overwrite-backup-<ts>/` and re-run with smart-rebase scoped to A-class only |
| SQLite `PRAGMA integrity_check` reports errors after a manual rewrite | byte-level `sed` on `memory/main.sqlite` corrupted page offsets (string lengths changed) | Roll back `memory/main.sqlite` from backup, then use `UPDATE observations SET narrative = REPLACE(narrative, '<old>', '<new>')` etc. inside `sqlite3` (length-safe) and rebuild FTS: `INSERT INTO observations_fts(observations_fts) VALUES('rebuild')` |
| `ENOENT ... backup/targeting.js` | extension install corrupt / mismatched | `openclaw plugins install @chainofclaw/soul --dangerously-force-unsafe-install --force` |
| `data dir not writable` | `~/.claw-mem` owned by wrong uid | 1.2.2+ auto-falls-back to `~/.openclaw/state/coc-soul`; on older versions `export CLAW_MEM_DATA_DIR=~/.openclaw/state` and restart gateway |
