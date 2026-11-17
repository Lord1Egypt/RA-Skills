# Hermes wiring

Use [upstream Hermes](https://github.com/NousResearch/hermes-agent) as the agent runtime. Install this skill folder in the active Hermes profile's skills directory; keep its references and scripts together. Isolate the DeFi profile with its own home, credentials and `SOUL.md` rather than changing another assistant's identity. Follow the runtime's current install and model/provider setup before declaring Boomkin usable.

Hermes source reviewed at `2e24e06e` supports `HERMES_HOME`, native skills and `mcp_servers` entries in its configuration. Discover the installed release's commands with `hermes mcp --help`. For an explicitly selected OAuth provider, native `hermes mcp add <name> --url <url> --auth oauth` handles transport discovery and the interactive authorization flow. Alchemy's documented endpoint is `https://mcp.alchemy.com/mcp`. A client configuration example from another harness is not directly interchangeable with Hermes YAML.

A restricted server entry has this shape after native setup:

```yaml
mcp_servers:
  alchemy:
    url: https://mcp.alchemy.com/mcp
    enabled: true
    trust: untrusted
    tools:
      include: [ping, ethChainId, ethGetBlockByNumber]
      resources: false
      prompts: false
```

Use native tool names returned by the server's discovery response. This example is a minimal probe selection, not a complete operating configuration: Alchemy RPC/data also requires selecting the appropriate app. Allow `list_apps` and `select_app` explicitly when needed, review their returned fields locally and avoid displaying cached keys. Do not grant `create_app`, `update_allowlist`, `walletSendPreparedCalls` or `walletCreateSession` merely to enable research. An empty include list disables all tools; it is not unrestricted access.

Restart/reload the intended profile after changes. Inspect discovered tools and complete a harmless chain/read check. Hermes `mcp test` can exit successfully while reporting connection failures; the actual result and returned data determine readiness. A CLI available to Hermes' terminal tool is distinct from an MCP server and inherits that process's environment. Keep provider credentials scoped to the selected runtime and never persist them inside skill files.


## Coinbase through the official local MCP

The remote harness restriction does not prevent use of Coinbase's native local server. Reviewed CLI 0.0.7 accepts `coinbase mcp` over stdio without a `--stdio` flag. An unauthenticated initialize/tools-list handshake returned 32 tools; this proves discovery only, not account access.

A Hermes entry may use `command: coinbase`, `args: [mcp]` after installing the pinned official CLI. In its `env` set `COINBASE_CONFIG_DIR` to the intended private profile directory and `COINBASE_ENV` to a unique name starting with `live-`, such as `live-boomkin-demo`. Configure that same environment using `coinbase env live-boomkin-demo --key-file <private-file>`. Use a unique environment name per profile: CLI 0.0.7's OS keyring keys are scoped by environment name, not by configuration directory. A separate directory alone does not isolate credentials.

Discover and explicitly allow only the required native read tools:

| Tool | Parameters |
| --- | --- |
| `coinbase_products_get` | Required `product_id` string |
| `coinbase_products_list` | Optional `symbol`, `product_type`, `product_ids`, `limit`, `cursor` |
| `coinbase_portfolios_list` | Optional `portfolio_type` |
| `coinbase_portfolios_get` | Required `portfolio_id`; optional denomination `currency` |
| `coinbase_balance` | Optional `portfolio_id`, `show_zero`, `limit`, `cursor` |
| `coinbase_fees` | Optional `product_type` |

Names and schemas above came from the pinned CLI's discovery response. Start with product reads; private account reads need the user's intended credentials and scope. Exclude account/environment changes, orders, transfers and payment tools from research configuration. Do not count successful tool listing as authenticated access. Agentic Wallet is a separate runtime: no portable dedicated `AWAL_HOME` or profile override was verified; do not claim Hermes profile isolation automatically isolates its OS-level wallet session.
