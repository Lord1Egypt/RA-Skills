# `coc-soul did` — DID identity management

Every subcommand acts on on-chain state. Read operations are free; write operations cost gas. **Flag names below are verified against the live CLI** — earlier revisions of this doc had the wrong names (e.g. `--key-hash` → really `--key-id`, `--cid` → really `--document-cid`).

## Preconditions for any write

1. `backup.didRegistryAddress` is configured
2. signer / private key is loaded and funded
3. target IDs / addresses are validated (bytes32 or 0x-address shape)

If `didRegistryAddress` is missing, every write subcommand fails early.

## Read commands (default first stop, no gas)

```bash
openclaw coc-soul did keys --agent-id <agentId> --json
openclaw coc-soul did delegations --agent-id <agentId> --json
```

Always `keys` / `delegations` **before** `revoke-*` / `update-*` to confirm the current state.

## Key management (write)

### Add a verification method

```bash
openclaw coc-soul did add-key \
  --agent-id <agentId> \
  --key-id <bytes32> \
  --key-address 0x<address> \
  --purpose <bitmask>
```

`--purpose` bitmask:

| Bit | Purpose |
|---|---|
| `1` | auth |
| `2` | assertion |
| `4` | capability invocation |
| `8` | capability delegation |

Example for an auth + assertion key: `--purpose 3`.

### Revoke a verification method

```bash
openclaw coc-soul did revoke-key \
  --agent-id <agentId> \
  --key-id <bytes32>
```

### Update the DID document CID

```bash
openclaw coc-soul did update-doc \
  --agent-id <agentId> \
  --document-cid <bytes32>
```

## Delegation

### Grant

```bash
openclaw coc-soul did delegate \
  --delegator <agentId> \
  --delegatee <agentId> \
  --scope <bytes32> \
  --expires <unix-ts> \
  --parent <bytes32-or-zero> \
  --depth 0
```

`--depth`:
- `0` (default) — leaf delegation; delegatee cannot re-delegate
- `1..3` — allow transitive re-delegation up to that many additional layers

### Revoke one delegation

```bash
openclaw coc-soul did revoke-delegation --delegation-id <bytes32>
```

### Emergency revoke all

```bash
openclaw coc-soul did revoke-all-delegations --agent-id <agentId>
```

## Credentials

### Anchor

```bash
openclaw coc-soul did anchor-credential \
  --credential-hash <bytes32> \
  --issuer <agentId> \
  --subject <agentId> \
  --credential-cid <bytes32> \
  --expires <unix-ts>
```

### Revoke

```bash
openclaw coc-soul did revoke-credential --credential-id <bytes32>
```

## Ephemeral identities

### Create

```bash
openclaw coc-soul did create-ephemeral \
  --parent <agentId> \
  --ephemeral-id <bytes32> \
  --ephemeral-address 0x<address> \
  --scope <bytes32> \
  --expires <unix-ts>
```

### Deactivate

```bash
openclaw coc-soul did deactivate-ephemeral --ephemeral-id <bytes32>
```

## Lineage + capabilities

### Record lineage (fork relationship)

```bash
openclaw coc-soul did record-lineage \
  --agent-id <agentId> \
  --parent <agentId> \
  --fork-height <n> \
  --generation <n>
```

### Update capability bitmask

```bash
openclaw coc-soul did update-capabilities \
  --agent-id <agentId> \
  --capabilities <uint16>
```

## EIP-712 signing

Delegation and credential anchoring use EIP-712 structured signatures. The CLI constructs the typed-data domain automatically using the configured RPC + `didRegistryAddress`. No manual signature flag is needed (`anchor-credential` does **not** take `--sig`).

## Easy-to-confuse flag map (real CLI vs old / sibling names)

| You might type | Actual flag |
|---|---|
| `--key-hash` | `--key-id` |
| `--verification-address` | `--key-address` |
| `--cid` (for update-doc) | `--document-cid` |
| `--parent-agent-id` (for record-lineage) | `--parent` |
| `--sig` (for anchor-credential) | (does not exist — signing is automatic) |

If you're unsure, run `openclaw coc-soul did <subcommand> --help` to confirm.

## DID is not backup

DID writes change identity-layer state (keys / delegations / credentials / lineage). They do **not** restore files or memory. For "recover this agent on another machine", see `references/backup.md` (restore path) or `references/guardian-recovery.md` (resurrection path).
