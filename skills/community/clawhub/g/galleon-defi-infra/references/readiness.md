# Readiness diagnostics

The [bundled helper](../scripts/readiness.ts) sends only `eth_chainId` and `eth_getBlockByNumber` with `["latest", false]`. It never loads a wallet, signs, creates accounts, resolves arbitrary tool names, pays an HTTP 402 or submits transactions. No endpoint URL, credentials, raw server errors or response bodies appear in its output.

With the npm package installed and the full endpoint supplied privately in `DEFI_RPC_URL`:

```bash
defi-infra-skills presence --json
defi-infra-skills doctor --chain-id 8453 --json
```

`--rpc-env NAME` selects a different existing environment variable, for example `LP_RPC_URL`; it never prints its value. `--max-age-seconds 120` overrides the default freshness threshold (1 to 86400 seconds). Set a chain-appropriate threshold before interpreting results. Presence reports are local observations only, not proof of authentication, quota or access.

If only the standalone skill is installed, Bun can import the helper directly:

```bash
bun -e 'import { diagnoseRpc } from "./scripts/readiness.ts"; const r = await diagnoseRpc({rpcUrl: process.env.DEFI_RPC_URL, chainId: 8453}); console.log(JSON.stringify(r)); process.exitCode = r.ok ? 0 : 1;'
```

Run from the installed skill directory. The npm CLI is built for Node 20+; the standalone TypeScript helper needs Bun. Upstream wallet CLIs have separate, newer Node requirements.

Network bounds: at most two sequential requests; five seconds each including body read; 64 KiB response maximum; redirects refused; no retry; HTTPS except literal localhost/127.0.0.1/IPv6 loopback over HTTP. Only probe the endpoint the user selected. RPC queries may consume provider quota even though they do not change chain state.

| Result | Interpretation |
| --- | --- |
| `ready` | Endpoint reports the intended chain and a sufficiently recent latest block |
| `missing_rpc` / `invalid_config` | Supply or correct private endpoint/chain/threshold configuration |
| `chain_mismatch` | Wrong network; no second RPC call is made |
| `stale_block` / `future_block` | Investigate provider lag, local clock, sequencer state or threshold |
| `http_error` / `rpc_error` | Check account access, quota and provider health without exposing response details |
| `invalid_response` / `request_failed` | Unsupported response, oversized body, transport failure or timeout |

A successful probe does not establish finalized state, complete indexing, archive access, balances, signer authority or profitability. State those remaining limitations when handing off to another workflow.
