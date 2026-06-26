# Carrier operations

A **carrier** is a hosting node that can adopt and run an offline agent's soul. Carriers are discovered on-chain through `CarrierRegistered` events.

## Registration

| Command | Effect |
|---|---|
| `carrier register --carrier-id <id> --endpoint https://… --cpu-millicores 1000 --memory-mb 2048 --storage-mb 10240` | Publish availability on-chain |
| `carrier deregister --carrier-id <id>` | Remove |
| `carrier availability --carrier-id <id> --available <true\|false>` | Flip the available flag without deregistering |

## Discovery

- `carrier list` — scan `CarrierRegistered` / `CarrierDeregistered` events (auto-chunked by 10000 blocks since 1.0.8)
- `carrier info --carrier-id <id>` — fetch full record for a specific carrier

## Daemon

The carrier daemon watches its inbox of pending resurrection requests and orchestrates the agent spawn.

| Command | Effect |
|---|---|
| `carrier start` | Start the daemon (requires `backup.carrier.enabled: true` in config) |
| `carrier stop` | Graceful shutdown |
| `carrier status` | Is the daemon enabled + running? |
| `carrier submit-request --request-id <id>` | Hand a specific pending request to the local daemon |

## Resurrection inside the daemon

For each pending request the daemon:

1. Verifies the carrier has been explicitly confirmed by guardians
2. Downloads the agent's latest soul backup from IPFS
3. Decrypts with the resurrection key (provided by the initiating guardian)
4. Spawns the agent using `carrier.agentEntryScript` in `carrier.workDir`
5. Reports back on-chain that the agent is alive

## Configuration

See `backup.carrier.*` in the soul config schema. Critical knobs:

- `enabled` (default `false`) — safety gate
- `carrierId` — your on-chain carrier ID
- `agentEntryScript` — path to the script that boots an agent from unpacked state
- `workDir` (default `/tmp/coc-resurrections`, **strongly recommend overriding** to a persistent path like `~/.openclaw/state/coc-soul/carrier` — `/tmp` is wiped on reboot mid-resurrection)
- `pollIntervalMs` (default 60000)
- `readinessTimeoutMs` (default 86400000 = 24h)

## Preconditions checklist (before going live as a carrier)

1. `backup.carrier.enabled: true` in plugin config
2. `backup.carrier.carrierId` set to the bytes32 you registered on-chain
3. `backup.carrier.agentEntryScript` is an absolute path that exists and is executable
4. `backup.carrier.workDir` points to a **persistent** directory with enough disk for an extracted agent (NOT `/tmp` on a host with reboots)
5. The endpoint passed to `carrier register --endpoint` is actually reachable from the COC network
6. At least one resurrection drill completed end-to-end (initiate → approve → submit-request → agent boot)

## Failure-mode triage

| Symptom | Cause | Action |
|---|---|---|
| `carrier start` returns "carrier disabled" | `backup.carrier.enabled` is false | Set it true and restart the gateway |
| `carrier start` aborts with "missing carrierId / agentEntryScript" | required fields blank | Fill both in `~/.openclaw/openclaw.json` `plugins.entries.coc-soul.config.backup.carrier` |
| Carrier registered but `carrier list` doesn't show it | RPC pointed at wrong network OR event scan range too small | Check `backup.rpcUrl` matches the chain you registered on; for ancient carriers add `--from-block 0` |
| Daemon receives request but agent never boots | `agentEntryScript` exits non-zero, or `workDir` runs out of disk | Check daemon logs; verify `workDir` is on a writable, large-enough volume |
| Resurrection request stuck "awaiting carrier confirmation" | guardian quorum hasn't approved yet | `coc-soul guardian status --request-id <id>` to see approval count vs threshold |

## Security

- Carrier hosts run resurrected agent code with full state access. Treat the host as production.
- Use least-privilege: a dedicated user, restricted `agentEntryScript`, tight `plugins.allow` whitelist.
- Never accept resurrection-key fragments via chat. Out-of-band channels only.
