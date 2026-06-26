# `backup.*` + `carrier.*` config schema

Read from `~/.chainofclaw/config.json` (or `$COC_SOUL_CONFIG`). The skill looks at the `backup` key; carrier config lives nested under `backup.carrier`.

```json
{
  "backup": {
    "enabled": true,
    "sourceDir": "~/.openclaw",
    "rpcUrl": "http://localhost:18780",
    "ipfsUrl": "http://localhost:5001",
    "contractAddress": "0x...SoulRegistry...",
    "didRegistryAddress": "0x...DIDRegistry...",
    "rpcAuthToken": "optional-for-gated-rpcs",
    "privateKey": "0x...",
    "autoBackup": true,
    "autoBackupIntervalMs": 3600000,
    "maxIncrementalChain": 10,
    "encryptMemory": false,
    "encryptionPassword": "...",
    "backupOnSessionEnd": true,
    "semanticSnapshot": {
      "enabled": true,
      "tokenBudget": 8000,
      "maxObservations": 50,
      "maxSummaries": 10
    },
    "categories": {
      "identity": true,
      "config": true,
      "memory": true,
      "chat": true,
      "workspace": true,
      "database": true
    },
    "carrier": {
      "enabled": false,
      "carrierId": "0x...",
      "agentEntryScript": "/path/to/agent-boot.sh",
      "workDir": "/tmp/coc-resurrections",
      "watchedAgents": [],
      "pollIntervalMs": 60000,
      "readinessTimeoutMs": 86400000,
      "readinessPollMs": 30000
    }
  }
}
```

## Critical fields

| Field | Required? | Notes |
|---|---|---|
| `rpcUrl` | yes | Must reach a COC node (local or public testnet) |
| `contractAddress` | yes for write | SoulRegistry deployment address |
| `didRegistryAddress` | yes for DID ops | |
| `ipfsUrl` | yes for backup | Default `http://127.0.0.1:5001` (local Kubo) |
| `privateKey` | yes for write | Use `chmod 600` on the config file |

## Key handling

For testnet the anvil default key works fine. For mainnet:

- Do **not** commit this file to git
- Prefer hardware signer or cloud KMS (not currently supported by the CLI — in roadmap)
- Keep the file mode `600`

## Backup chain limit

`maxIncrementalChain: 10` means after 10 incremental backups, the next one is forced to full. This bounds restore time.

## Where config actually comes from (OpenClaw plugin mode)

When running through `openclaw coc-soul ...` (plugin mode), the **authoritative** source is `~/.openclaw/openclaw.json` under:

```jsonc
{
  "plugins": {
    "entries": {
      "coc-soul": {
        "enabled": true,
        "config": {
          "backup": {
            // ...same shape as the standalone schema above...
          }
        }
      }
    }
  }
}
```

The standalone `coc-soul` bin still reads `~/.chainofclaw/config.json` / `$COC_SOUL_CONFIG`, but in plugin mode plugin config wins.

## Minimal viable config (testnet)

`coc-soul` ships testnet defaults for `rpcUrl` / `ipfsUrl` / `contractAddress` / `didRegistryAddress` / `faucetUrl`. Minimal explicit config:

```jsonc
{
  "plugins": {
    "entries": {
      "coc-soul": {
        "enabled": true,
        "config": {
          "backup": { "enabled": true }
        }
      }
    }
  }
}
```

If `backup.privateKey` is absent, soul auto-generates an agent EOA + auto-drips testnet COC. First `openclaw coc-soul backup init` works immediately.

## dataDir + keystore resolution chains (1.2.2)

### Soul data dir (where keystore + scratch land)

Priority — first writable wins, fail-fast EACCES with a copy-paste fix at the bottom:

1. `plugins.entries.coc-soul.config.backup.dataDir`
2. `$CLAW_MEM_DATA_DIR` (shared with @chainofclaw/claw-mem)
3. `$OPENCLAW_STATE_DIR/coc-soul`
4. `~/.claw-mem` (default, shared with claw-mem)
5. `~/.openclaw/state/coc-soul` (1.2.2+ auto-fallback when default's parent is owned by the wrong uid — typical multi-user Docker host)

No `/tmp` fallback for durable identity state.

### Keystore (agent.key) priority

1. explicit `keyPath` (internal call sites)
2. `$COC_SOUL_KEYSTORE_PATH`
3. `$OPENCLAW_STATE_DIR/coc-soul/keys/agent.key`
4. `~/.claw-mem/keys/agent.key`

File mode is enforced to `0600` on write.

## Recommended overrides (production)

- `backup.privateKey` — supply explicitly only if you don't want auto-generated keystore
- `backup.encryptMemory: true` + `backup.encryptionPassword` — encrypt the memory payload before IPFS upload (otherwise it's plaintext at the CID)
- `backup.carrier.workDir` — override the default `/tmp/coc-resurrections` to a persistent path (e.g. `~/.openclaw/state/coc-soul/carrier`); `/tmp` is wiped on reboot mid-resurrection
- `plugins.allow: ["claw-mem", "coc-soul", "coc-node"]` — explicit trusted plugin list at the openclaw.json root, so the gateway stops warning `plugins.allow is empty`

## Docker / container deployment

- One persistent volume must back the soul data dir. If container FS is ephemeral, mount a host path for `~/.claw-mem` or set `CLAW_MEM_DATA_DIR` to mounted storage.
- If the in-container scheduler is unavailable, drive periodic `backup heartbeat` from the host (cron / systemd timer that calls `docker exec`).

## Failure-mode triage

| Symptom | Cause | Action |
|---|---|---|
| `data dir not writable` at activation | `~/.claw-mem` owned by another uid | 1.2.2+ auto-falls-back to `~/.openclaw/state/coc-soul`; older versions: `export CLAW_MEM_DATA_DIR=~/.openclaw/state` and restart |
| `backup` reports "not configured" | missing `contractAddress` or `privateKey` for the active network | `backup doctor --json` shows which field is empty |
| Carrier daemon no-ops | `backup.carrier.enabled: false` or required fields blank | Set both, restart |
| Unexpected key source loaded | env var override winning over config | Print `openclaw coc-soul did keys --agent-id <id>` to confirm; check `$COC_SOUL_KEYSTORE_PATH` and `$OPENCLAW_STATE_DIR` |
| `[gateway] plugins.allow is empty` warning | no allow-list set | `jq '.plugins.allow = ["claw-mem","coc-soul","coc-node"]' ~/.openclaw/openclaw.json > /tmp/oc && mv /tmp/oc ~/.openclaw/openclaw.json` |
