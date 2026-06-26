---
name: coc-soul
description: Give an AI agent a persistent on-chain soul — register and manage a decentralized identity (DID), encrypt and anchor agent state to IPFS + SoulRegistry, configure guardians for social recovery, and enable cross-carrier resurrection so the agent can resume on a different device if the host dies. **Pairs with `claw-mem2db` to deliver "digital / silicon-based persistence" for AI agents**: when claw-mem is co-installed, every backup automatically captures claw-mem's chat history + tool-call observations + session summaries as a token-budgeted semantic snapshot, so an agent recovered on a fresh host can replay its memory context — not just its files. Soul also runs fully standalone (without claw-mem), in which case backups still cover identity / config / workspace / chat files but skip the semantic snapshot. Use when the user wants their AI agent to survive device loss, transfer ownership, delegate capabilities, run a guardian / carrier node, inspect on-chain identity state, or get persistent cross-device memory paired with claw-mem. Zero-config on COC testnet — installation auto-generates an EOA keystore (~/.claw-mem/keys, shared with claw-mem; or $OPENCLAW_STATE_DIR/coc-soul/keys in sandboxed hosts), auto-drips testnet COC from the public faucet for gas, and pre-fills RPC + IPFS + contract addresses for the live testnet. The first `openclaw coc-soul backup init` works with no manual setup.
version: 1.2.10
metadata:
  openclaw:
    homepage: https://www.npmjs.com/package/@chainofclaw/soul
    primaryEnv: CLAW_MEM_DATA_DIR
    requires:
      bins:
        - node
      anyBins:
        - coc-soul
        - openclaw
    install:
      - kind: node
        package: "@chainofclaw/soul"
        version: "1.2.6"
        bins:
          - coc-soul
---

# coc-soul — agent identity, backup, and resurrection

The **soul layer** for AI agents: on-chain DID, encrypted backups to IPFS, social recovery via guardians, and cross-device resurrection via carriers. Backed by the npm package [`@chainofclaw/soul`](https://www.npmjs.com/package/@chainofclaw/soul) which ships both a standalone `coc-soul` CLI and an OpenClaw skill (id `coc-soul`).

Soul works **standalone** (backs up the agent's home tree to chain + IPFS), and gets one extra capability when **`claw-mem2db` is installed alongside it**: each backup also captures claw-mem's chat history, tool-call observations, and session summaries as a token-budgeted semantic snapshot. Recover on a fresh host and the agent gets back not just its files but its remembered context — chat preferences, decisions, conversation history. **This is the "digital / silicon-based persistence" story.**

---

## 30-second decision tree (operators read here first)

If the user is asking "how do I recover on another machine?", pick **one** path before saying anything else:

1. **Have backup material (manifest CID or `~/.openclaw/.coc-backup/latest-recovery.json`)** → use the **restore** path: `openclaw coc-soul backup restore ...`
2. **Lost the owner key OR need to migrate ownership** → use **resurrection** (owner-key) or **guardian social recovery**

Don't merge the two explanations until the path is selected. `recovery` and `resurrection` are different flows (see `references/guardian-recovery.md`).

## Critical CID terminology (avoid confusion)

| Term | Meaning | Use it for |
|---|---|---|
| `manifest CID` / `latestManifestCid` | Backup restore point (IPFS manifest) | `backup restore --manifest-cid <cid>` |
| full-backup CID | Earlier baseline snapshot | Roll back to a baseline state |
| latest incremental CID | Newest chain tip | Restore the latest state |
| identity CID / hash | Identity-content hash used in registration | **Not** the backup restore point |

Rule: when a user asks "what's your CID?", first confirm whether they mean the **latest backup manifest CID** vs. an older backup CID vs. the identity registration CID — they get conflated constantly.

## Key material — agent safety rules

| Secret / role | Purpose | Needed when | Chat-safe? |
|---|---|---|---|
| owner key / agent operator key | normal chain ops, backup anchor | daily ops | **Never paste in chat** |
| resurrection key | owner-key resurrection flow | `resurrection start` | **Never paste in chat** |
| guardian accounts | social recovery approvals | `recovery approve/complete` | addresses yes; **private keys never** |

**Hard rule for any agent reading this skill:** never request, transmit, or echo private keys in chat — including "split" or "encrypted" fragments. Always route key transfer to a local secure channel.

## Ultra-quick runbook (10 lines)

1. Pick the path first: `restore` or `resurrection` (see the decision tree above).
2. Run `openclaw coc-soul backup doctor --json` and read `chain.registered` / `restore.available` / `resurrection.configured`.
3. If there's a manifest CID or a `latest-recovery.json`, take the **restore** path.
4. **Restore to `/tmp/...` first** — never overwrite a production directory in one step.
5. Verify `merkleVerified: true` + exit code 0, then promote to the production path only after explicit user confirmation.
6. No owner key but resurrection was pre-configured → take the **resurrection** flow.
7. Need multi-party approval for ownership migration → take **guardian recovery** (quorum + timelock).
8. Script the `heartbeat` first, then schedule it via cron / systemd / OpenClaw scheduler.
9. Private keys never go through chat (including split / encrypted fragments or temporary paste).
10. Default command surface is `openclaw coc-soul ...`; the bare `coc-soul ...` only exists when the standalone bin was installed via `npm i -g @chainofclaw/soul`.

## Common failure → cause → fix

| Symptom | Likely cause | First action |
|---|---|---|
| `Unsupported state or unable to authenticate data` on restore | encryption mode / key mismatch | Re-read `encryptionMode` in `latest-recovery.json`: `password` mode requires `--password`; `privateKey` mode must NOT pass `--password` |
| `429 rate limit exceeded` from IPFS | manifest fetch is rate-limited | Exponential-backoff retry until `merkleVerified: true` |
| `[gateway] unauthorized (1008)` from cron / scheduled job | wrong gateway auth mode / token / proxy config | Fix gateway auth before scheduling anything |
| `[gateway] unauthorized (1008)` **right after a restore** | restore overlaid `gateway.auth.mode` from the source host; the old TUI command `--token "$(jq -r .gateway.auth.token ...)"` now resolves to the literal string `null` | Run `jq '.gateway.auth.mode'` to see the active mode and pick the matching flag (see the "Cross-host restore" section below). If the whole auth block was overwritten, copy `.gateway.auth.*` back from `~/.openclaw/.restore-overwrite-backup-*/openclaw.json` |
| `ENOENT ... backup/targeting.js` | extension install is missing files | Reinstall: `openclaw plugins install @chainofclaw/soul --dangerously-force-unsafe-install --force` |
| `data dir not writable` at startup | `~/.claw-mem` is owned by another uid (common Docker multi-user case) | 1.2.2+ auto-falls-back to `~/.openclaw/state/coc-soul`; on older versions `export CLAW_MEM_DATA_DIR=~/.openclaw/state` and restart the gateway |
| `plugins.allow is empty ... may auto-load` warning | gateway has no trusted-plugin allow list | Add `"plugins": {"allow": ["claw-mem","coc-soul","coc-node"]}` to `~/.openclaw/openclaw.json` |

Full per-command troubleshooting lives at the end of `references/backup.md` and `references/config.md`.

## Cross-host restore — read BEFORE you blanket-overwrite (1.2.4+)

The most dangerous restore scenario: backup made on host A (e.g. `$HOME=/home/node`), restoring on host B (`$HOME=/home/baominghao`). The backup's files contain absolute paths to host A; literal copies will (a) fake history, (b) corrupt SQLite if anyone tries byte-level `sed`, and (c) **wipe out host B's `gateway.auth` configuration**, locking the operator out with a 1008 right after restart.

**The agent must ask the user before any cross-host restore.** Don't auto-overwrite. Three-class policy:

| Class | What | Example fields | What restore does |
|---|---|---|---|
| **A. Runtime config (paths)** | Where on disk to read/write today | `agentDir`, `models.json` paths, `latest-recovery.json` `targetDir` | **Rewrite** old `$HOME` → new `$HOME`, structured (JSON parse, not `sed`) |
| **B. Historical content** | Records of past events | `sessions/*.jsonl`, `observations.{narrative,facts,files_*}`, `semantic-snapshot.json` | **Leave intact**. Rewriting fakes history. claw-mem doesn't blindly open these paths anyway. |
| **C. Host-local policy** | Belongs to **this** host's operator | `gateway.auth.*`, `gateway.bind`, `gateway.port`, `plugins.allow`, target-host provider keys | **Preserve target host's existing values** — never overlaid by backup |

**Auth-mode warning, in particular:** `gateway.auth.mode` and `.token` / `.password` belong to the host, not the agent. After restoring, always re-check:

```bash
jq '.gateway.auth.mode' ~/.openclaw/openclaw.json
```

Pick the matching TUI flag — `--token` only works when `mode = "token"` AND `.token` is non-null. If the active mode is `password` or `trusted-proxy`, `jq -r .gateway.auth.token` returns the literal string `"null"` and TUI sends that, which the gateway rejects with 1008. **Don't reflexively use `--token` after a restore — read the active mode first.**

Full procedure with command-line examples: `references/backup.md` → "Cross-host restore: directory-mismatch handling" + "Auth-mode preservation rule".

## Post-backup messaging contract (1.2.6+)

**After every successful `backup create`, the agent MUST relay the recovery info to the user.** The CLI 1.2.6+ prints it; agents that wrap the CLI must pass it through, not swallow it. The user needs four things to be able to restore later:

1. **The manifest CID** (`b.manifestCid`, e.g. `bafy...`) — what to ask for at restore time.
2. **The signing-key location** — where the private key needed to read the encrypted backup lives. One of:
   - `~/.claw-mem/keys/agent.key` (default keystore, mode `0600`, auto-generated when `backup.privateKey` is unset; resolution chain: `$COC_SOUL_KEYSTORE_PATH` → `$OPENCLAW_STATE_DIR/coc-soul/keys/agent.key` → `~/.claw-mem/keys/agent.key`)
   - `backup.privateKey` in `~/.openclaw/openclaw.json` (when operator set it explicitly)
3. **The encryption mode** — `none` / `privateKey` / `password` — determines whether `--password` is needed at restore time.
4. **The recovery package path** — `<sourceDir>/.coc-backup/latest-recovery.json` — small JSON file with all of the above pre-formatted; copy this off-host alongside the key for fast restore.

The CLI emits this block:

```
Backup complete (full):
  manifest:   bafyabc...
  files:      127
  bytes:      4194304
  merkleRoot: 0xabc...
  txHash:     0xdef...

Recovery info — keep this safe to restore on another host:
  recovery package: /home/<user>/.openclaw/.coc-backup/latest-recovery.json
  encryption mode:  privateKey
  signing key file: /home/<user>/.claw-mem/keys/agent.key (mode 0600 — copy off-host securely)
  signer address:   0x...

To restore on another host (always restore to /tmp first, verify, then promote):
  openclaw coc-soul backup restore --manifest-cid bafyabc... \
    --target-dir /tmp/openclaw-restore-test

  (if you also have /home/<user>/.openclaw/.coc-backup/latest-recovery.json on the target host:)
  openclaw coc-soul backup restore --latest-local --target-dir /tmp/openclaw-restore-test
```

**Agent responsibilities when displaying this:**

- Echo the **manifest CID** verbatim (it's how the user later asks "restore my backup `bafy...`")
- Echo the **signing key file path** verbatim — this is the file the user must back up off-host (encrypted USB / passphrase-protected vault / hardware security module). **Do NOT print the key contents themselves.**
- Echo the **`To restore on another host`** block verbatim — operators on the recovery host will copy-paste it
- If the encryption mode is `password`, remind the user that `--password '<value>'` is required at restore time and they must remember it (or store it securely separately)

For agents running headless (no user attention right now): the same info is persisted to `~/.openclaw/.coc-backup/latest-recovery.json` automatically — operators can read it later via `cat` or `openclaw coc-soul backup status --json`.

---

## Relationship with claw-mem2db

claw-mem and coc-soul are **separate, decoupled skills**. Each works on its own; together they cover complementary halves of "agent persistence":

| Skill | Owns | What changes when paired |
|---|---|---|
| [claw-mem2db](https://clawhub.ai/ngplateform/claw-mem2db) | Local memory: chat + tool capture, FTS5 search, hybrid recall, in-process injection | Claw-mem itself doesn't change. Soul opportunistically reads the SQLite DB. |
| **coc-soul** | On-chain DID, IPFS backup, guardian recovery, carrier resurrection | When claw-mem's DB is detected at startup, every backup adds a `semantic-snapshot.json` slice (top-N observations + summaries within `tokenBudget`) to the manifest. On recovery, that snapshot is restored alongside the rest of the agent home. |

**Detection is automatic and silent.** At plugin activation, soul probes the same dataDir chain claw-mem uses (`$CLAW_MEM_DATA_DIR` → `$OPENCLAW_STATE_DIR/claw-mem` → `~/.claw-mem`) and logs one of two lines:

- `[coc-soul] claw-mem detected at <path> — semantic snapshot ... will be included in each backup`
- `[coc-soul] claw-mem not detected — backups will skip the semantic snapshot (install @chainofclaw/claw-mem alongside soul to enable memory replay on recovery)`

No coupling at the npm-dependency level: soul does not depend on the `@chainofclaw/claw-mem` package. It just opens the SQLite DB read-only when present and reads two tables (`observations`, `session_summaries`). If the DB schema is absent or unreadable, soul logs a warning and moves on — backup never fails because of a memory hiccup.

## Data dir alignment with claw-mem (1.2.0+)

Soul writes its own files (keystore, config.json) to the same root as claw-mem by default — `~/.claw-mem` — so the two plugins share one operator-managed directory. Resolution priority (matches claw-mem's chain):

1. `plugins.entries.coc-soul.config.backup.dataDir` (per-instance plugin config, when set)
2. `$CLAW_MEM_DATA_DIR` (shared with claw-mem)
3. `$OPENCLAW_STATE_DIR/coc-soul` (sandboxed-host fallback, soul-specific subdir)
4. `~/.claw-mem` (default)
5. `~/.openclaw/state/coc-soul` (1.2.2+ auto-fallback when the default is owned by the wrong uid — typical multi-user Docker host)

If none of these are writable, soul **fails fast at activation** with a copy-paste-ready EACCES message (each candidate path, the resolved `getuid()` + `HOME`, and a one-line fix). No silent `/tmp` fallback. No half-broken backup runs.

## Mental model

Every AI agent is identified by a `bytes32 agentId`, controlled by an EOA (owner). The skill covers five concerns:

| Area | What it does |
|---|---|
| **DID** | Register the agent on-chain, manage verification methods (keys), delegate capabilities, anchor verifiable credentials, record lineage (fork relationships) |
| **Backup** | Encrypt + upload agent state (identity / config / memory / chat / workspace / DB) to IPFS, anchor the manifest CID in SoulRegistry. With claw-mem present, also includes a token-budgeted semantic snapshot of recent observations + summaries. |
| **Guardian** | Designate trusted accounts that can jointly recover or resurrect the agent |
| **Recovery** | Social recovery flow — guardians collectively migrate the owner to a new address. The semantic snapshot rides along, so the recovered agent gets its memory context back too. |
| **Carrier** | Register a hosting node that can resurrect offline agents |

## Zero-config on COC testnet (1.1.6+)

**Out of the box, no setup is required to run against COC testnet.** A fresh `openclaw plugins install @chainofclaw/soul` lands an agent that can immediately query the chain, register a soul, and run backups. Specifically, on first activation the plugin:

1. **Auto-generates an agent EOA** if `backup.privateKey` is empty. The key file is written with mode `0o600` to one of (in priority order):
   - `$COC_SOUL_KEYSTORE_PATH` (operator override)
   - `$OPENCLAW_STATE_DIR/coc-soul/keys/agent.key` (set by OpenClaw inside its sandbox — the typical path)
   - `~/.claw-mem/keys/agent.key` (standalone default)

   The chosen path and resulting agent address are logged: `[coc-soul] auto-generated agent key at <path>` and `[coc-soul] agent address: 0x…`.

2. **Auto-drips testnet COC** to the new EOA from the public faucet (`backup.faucetUrl` defaults to `http://199.192.16.79:3003`, 10 COC per drip, 24h per-address cooldown). Logs: `[coc-soul] faucet dripped 10.0 COC to 0x… (tx 0x…)`. So the very first `openclaw coc-soul backup init` already has gas.

3. **Defaults `rpcUrl`, `ipfsUrl`, `contractAddress`, `didRegistryAddress`** to the live COC testnet (RPC `199.192.16.79:28780`, IPFS `199.192.16.79:28786`, deployed SoulRegistry / DIDRegistry).

**You do NOT need to set any of these manually for testnet usage.** The agent should `openclaw coc-soul backup init` directly. Override fields only when targeting mainnet, a private testnet, or an existing wallet.

To bypass the keystore (e.g. use a wallet you already have): set `backup.privateKey` in config. To disable the auto-faucet (mainnet): set `backup.faucetUrl: ""`.

## How to invoke

**Inside OpenClaw (recommended — works automatically after `plugins install`):**

```bash
openclaw coc-soul backup status
openclaw coc-soul did delegations --agent-id 0x...
```

**Standalone bin (only if you ran `npm i -g @chainofclaw/soul` separately):**

```bash
coc-soul backup status
```

> `openclaw plugins install` does NOT install the standalone `coc-soul` binary into your PATH. Use `openclaw coc-soul ...` (with the `openclaw` prefix), or install the bin globally via npm if you want the bare command.

## Typical flows

1. **First-time soul registration + backup (zero config)** — Just run `openclaw coc-soul backup init`. The plugin auto-generates the agent EOA, auto-drips testnet COC for gas, then registers on SoulRegistry and runs the first full backup. No manual privateKey, no manual faucet, no manual contract addresses. Watch the activation logs to see the chosen keystore path and the agent address.
2. **Periodic incremental backup** — `openclaw coc-soul backup create` (auto runs hourly if `backup.autoBackup: true`).
3. **Inspect agent state** — `openclaw coc-soul backup status` (summary), `openclaw coc-soul backup doctor` (actionable recommendations).
4. **Delegation** — `openclaw coc-soul did delegate --delegator <agentId> --delegatee <targetId> --scope <hash> --expires <epoch> --depth 0`.
5. **Guardian setup** — `openclaw coc-soul guardian add --agent-id <id> --guardian 0x...` (repeat for each guardian).
6. **Emergency recovery** (you lost your owner key) — a guardian runs `openclaw coc-soul recovery initiate`, the quorum approves via `recovery approve`, then after timelock `recovery complete`.
7. **Resurrection as carrier** — `openclaw coc-soul carrier register --endpoint https://...` on the hosting node; `openclaw coc-soul carrier start` runs the daemon.

## When NOT to use this skill

- Running a COC chain node yourself — use [coc-node](https://clawhub.ai/ngplateform/coc-node).
- Local semantic memory **only** (no chain backup needed) — use [claw-mem2db](https://clawhub.ai/ngplateform/claw-mem2db) on its own. Add coc-soul on top later if you decide you want the data on-chain.
- Smart contract deployment — that lives in the [COC source repo](https://github.com/NGPlateform/COC) `contracts/` tree.

## Reference

Detailed references live alongside this file:

- `references/did.md` — full `did` subcommand tree, delegation semantics, ephemeral identities, credentials, lineage
- `references/backup.md` — backup / restore / prune flows, encryption, semantic snapshot, categories
- `references/guardian-recovery.md` — guardian lifecycle + social recovery timelock + quorum rules
- `references/carrier.md` — carrier registration, daemon modes, resurrection request flow
- `references/config.md` — complete `backup.*` + `carrier.*` config schema

Source and issue tracker: <https://github.com/NGPlateform/claw-mem/tree/main/packages/soul>.
