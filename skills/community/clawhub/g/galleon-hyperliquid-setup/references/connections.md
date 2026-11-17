# Connections and first run

## Public market access

The official public API needs no account, API wallet, signature, or npm package:

- Mainnet: `https://api.hyperliquid.xyz/info`
- Testnet: `https://api.hyperliquid-testnet.xyz/info`
- Send JSON with HTTP POST. This `/info` operation reads data; it does not submit a trade.

For the validator-operated perpetual ETH market, send these bodies separately:

```json
{"type":"metaAndAssetCtxs"}
```

```json
{"type":"l2Book","coin":"ETH"}
```

Match `universe[i].name` to the exact coin and use context at the same index. The
bundled helper rejects a missing/mismatched market, malformed numbers, empty/crossed
book, and old/future book timestamps. Network requests have a timeout and size cap.
This helper is limited to validator-operated perpetual markets. HIP-3 and spot
require their separate metadata contracts through an appropriate read adapter.
Metadata indices here must not be reused as universal exchange asset IDs.

The helper returns raw reported funding with no implied interval or return forecast.
It is a first-read diagnostic, not a trading signal or account-risk assessment.
Use `hyperliquid-analyze` for interpretation and strategy evaluation.

## Harness connection

Hermes, OpenClaw, Eve, Codex, Claude Code, and other harnesses expose different tool
names. Discover the actual tool schemas. A browser can fetch documentation but may
not POST JSON; a shell with Node can run the helper; an HTTP tool can use the bodies
above. Never claim HTTP capability until a read succeeds.

If the harness has neither, report the missing HTTP or shell capability and direct
the user to its native tool settings. Do not install an arbitrary trading MCP server
or change permissions automatically. The standard skill installer does not install
or authenticate execution tools.

## Account and execution access

The public user address is enough for supported account reads. An API wallet address
is not the user account address. Use the existing read adapter's declared supported
account modes and retain the requested account across handoffs.

Execution needs an already configured tool that owns signing outside the agent's
context, serializes nonces, supports explicit account/network selection, accepts an
approved ticket, sends once, and returns order IDs/raw response for reconciliation.
Ask the harness to enumerate tool schemas and run a non-submitting validation or
fixture test first. If these capabilities are missing, analysis can continue but
execution remains unavailable. Building that integration belongs to
`hyperliquid-engineer`; installing these skills alone does not build it.

The official Python SDK provides `Info` read methods and exchange integrations.
Use its read-only `Info` surface without copying credential examples. Secret loading
and API-wallet approval are outside this skill.

## First result

Report the network, exact coin, observation time, book age, mark/oracle prices,
spread, raw funding, data gaps, and next skill. Preserve the provenance request
bodies. Never label fixture data live or reuse it for a real ticket.

Sources checked 2026-09-05:
[official SDK Info methods](https://github.com/hyperliquid-dex/hyperliquid-python-sdk/blob/master/hyperliquid/info.py),
[official SDK network constants](https://github.com/hyperliquid-dex/hyperliquid-python-sdk/blob/master/hyperliquid/utils/constants.py),
[official API documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api).
