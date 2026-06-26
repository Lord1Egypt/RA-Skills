# `~/.chainofclaw/config.json` schema

`coc-node` reads `$COC_NODE_CONFIG` if set, otherwise `~/.chainofclaw/config.json`. Missing keys fall back to defaults baked into the package.

```json
{
  "dataDir": "~/.chainofclaw",
  "node": {
    "enabled": true,
    "defaultType": "dev",
    "defaultNetwork": "local",
    "port": 18780,
    "bind": "127.0.0.1",
    "autoAdvertiseStorage": true
  },
  "storage": {
    "quotaBytes": 268435456,
    "advertisedBytes": 268435456,
    "reservedBytes": 268435456,
    "enforceQuota": true,
    "reserveFile": ".quota.reserved"
  },
  "bootstrap": {
    "cocRepoPath": "/path/to/COC"
  }
}
```

## Field reference

### `dataDir` (string)

Where node registry and per-node data directories live. `~` is expanded.

### `node.*`

| Key | Type | Default | Notes |
|---|---|---|---|
| `enabled` | bool | `true` | Gate for the whole skill; set `false` to disable plugin activation |
| `runtimeDir` | string | (COC repo's `runtime/`) | Where to find `coc-agent.ts` / `coc-relayer.ts` |
| `defaultType` | enum | `dev` | Used when `--type` is omitted |
| `defaultNetwork` | enum | `local` | Used when `--network` is omitted |
| `port` | number | `18780` | RPC port default |
| `bind` | string | `127.0.0.1` | Bind address |
| `autoAdvertiseStorage` | bool | `true` | Auto-pick `advertisedBytes` when omitted |

### `storage.*`

| Key | Type | Default | Notes |
|---|---|---|---|
| `quotaBytes` | number | `268435456` | Hard cap for this process's disk usage |
| `advertisedBytes` | number | `268435456` | P2P network claim (min 256 MiB) |
| `reservedBytes` | number | `268435456` | Pre-allocate via `fallocate` to prevent over-commit |
| `enforceQuota` | bool | `true` | When `false`, skip the reservation check |
| `reserveFile` | string | `.quota.reserved` | Name of the placeholder file |

### `bootstrap.cocRepoPath` (string)

Absolute path to your COC source-repo clone. Required for `node start` (spawn needs `node/src/index.ts` etc.). Read-only commands tolerate this being unset.
