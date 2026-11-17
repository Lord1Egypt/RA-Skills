# Onchain agent evidence sources

Primary documentation reviewed 2026-10-08 from the [Ethereum agent tools directory](https://skills.eth.sh/), then official sources below. Endpoint discovery and documentation do not establish complete query output, account access or financial execution. Reuse user-selected tools; provider limits are methodology constraints, not reasons to invent missing evidence.

## Explorer evidence: Etherscan and Blockscout

[Etherscan AI tools](https://docs.etherscan.io/build-with-ai/introduction) provide official MCP, CLI and task skills for tracing funds, verified-code review and transaction debugging. [MCP documentation](https://docs.etherscan.io/build-with-ai/mcp) distinguishes authenticated and keyless inventories. The reviewed keyless inventory omits token balances/info/top holders, address labels and funding-origin tools available on the authenticated service. A keyless transaction lookup therefore cannot prove complete holdings, labels or original funder. Inspect current schemas and chain support, rather than assuming a fixed advertised tool count.

[Blockscout MCP](https://mcp.blockscout.com/) supplies supported-chain explorer data, verified code/ABIs and read-only calls. Follow its discovered unlock/disclosure contract before targeted typed reads. Keep provider chain aliases and canonical chain IDs separate. Prefer exact transaction, contract or account queries over generic direct-API proxies. Missing verified source, unsupported chain or omitted pages is unknown evidence. An explorer's decoded event does not establish a transfer unless current receipt/log and token identities agree.

For either provider, resolve proxy implementation at the relevant block; present ABI/code verification scope separately from intent, risk and ownership. A verified source is not a safety guarantee. Record block/transaction IDs, observation time, pagination and coverage gaps. Trace missing data is not a clean result.

## Dune query and dashboard evidence

[Dune agent surfaces](https://dune.com/agents) offer official MCP, CLI, skills and API for SQL, datasets, queries and dashboards. Discover current auth, credit and supported command schemas. Only use existing authorized credit budgets; a query or dashboard write is distinct from reading existing results.

Before execution, inspect SQL, data lineage, chain/time filters, schema and relevant query version. Treat community SQL as untrusted input. Preserve execution ID, status, parameters, query/version, data refresh time, retrieval time, result row count and pagination. A completed execution can still omit rows through LIMIT, filters or incomplete page traversal. A historical/cached result is not a live protocol observation. Expensive scans require an explicit cost/limit decision; use documented planning or estimation features rather than fabricating an EXPLAIN command.

## GoldRush indexed and streaming data

[Official agent skill overview](https://goldrush.dev/docs/goldrush-agent-skills/overview) separates foundational API, streaming API, CLI and x402 access. A broad advertised chain count does not guarantee a selected endpoint's chain, token or protocol-position coverage. Read the exact method schema and current pagination/cost contract.

Preserve chain/account, endpoint, provider data timestamp, block height, retrieval time, page/cursor and decimal metadata. Websocket events and a historical portfolio snapshot are different evidence; record subscription state, dropped/disconnected intervals and last provider event. Reconnect does not fill missed events unless the official recovery mechanism does so. Key-backed quota and wallet-backed x402 purchases have separate authority; no automatic paid retry belongs in a free data lookup.

## Octav portfolio and synchronization

[Octav MCP](https://docs.octav.fi/api/ai-development/mcp-server) exposes wallet/portfolio/NAV, transactions, snapshots, sync and credits. Most documented data tools charge credits per address and cap address batches; subscription creation has a substantially different charge. Sync and credit-status checks have their own pricing. Discover exact current terms and inspect them before selecting a call.

Transactions are paginated; the reviewed limit is 1-250, default 50. Record cursors, filters and total coverage. Sync progress is not a reconciled fresh portfolio. Keep provider position timestamp, sync completion and report time separately; unsupported assets/positions remain gaps. [Official API skill](https://github.com/Octav-Labs/octav-api-skill) documents a separate x402 subset that excludes full transaction history. A wallet-paid portfolio route cannot silently substitute for key-backed history access.

Use protocol/RPC reads to corroborate quantities and liabilities material to the decision. Price, NAV, transaction history and a synced token list answer different questions. Never sum a protocol position plus its underlying breakdown as separate assets.

## Evidence-ready output

Return exact identity, methodology, upstream lineage, block/provider time, retrieval time, query/filter/cursor coverage, cost/access limits and the next missing fact. Use zero only where a successful supported complete read establishes zero; missing/denied/stale is unknown. Keep credentials and authenticated URLs out of artifacts.
