# Troubleshooting

## `node start` fails with "COC repo not located"

The skill can't find the COC source repo. Either:

- Set env var: `export COC_REPO_PATH=/absolute/path/to/COC`
- Or edit config: `coc-node config set bootstrap.cocRepoPath /absolute/path/to/COC`
- Or cd into the COC repo before running `coc-node` (auto-discovery walks upward)

Read-only commands (`list`, `status`, `config show`) do not need this.

## Port already in use

Default local port is 18780; default testnet port is 28780. On collision, pass `--rpc-port` explicitly. Other derived ports (`ws`, `p2p`, `wire`, `ipfs`) are offset from `rpcPort`; see `node config show <name>` to see exactly which ports a node uses.

## `storage-reservation` warn

`enforceQuota: false` in config disables the reservation. For production, keep `enforceQuota: true` and mount `dataDir` on a dedicated disk so the reservation file doesn't collide with OS or home-dir files.

## Node shows "STOPPED" after `node start`

- Check `coc-node node logs NAME --follow` — most startup failures print a clear reason
- Verify Node.js version ≥ 22 (`node -v`)
- Verify `COC_REPO_PATH` points at a complete clone (run `ls $COC_REPO_PATH/node/src/index.ts`)

## RPC status empty

If `coc-node node status NAME` shows `RUNNING` but no `blockHeight`/`peerCount`:

- The node is up but RPC hasn't finished starting — retry in a few seconds
- Or RPC bind is non-localhost and can't be reached from the calling process — inspect `rpcBind` / `rpcPort` in `config show`

## Removing stale registry entries

If a node process died without being removed from the registry:

```bash
coc-node node remove NAME --yes --keep-data  # deregister without touching data
```

Then `coc-node node install --name NAME` will create a fresh registry entry.
