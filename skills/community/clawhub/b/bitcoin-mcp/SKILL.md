---
name: bitcoin-mcp
description: "47 Bitcoin tools for your AI agent — fee intelligence, mempool analysis, address lookups, transaction decoding, and more. MCP server backed by the Satoshi API."
homepage: https://github.com/Bortlesboat/bitcoin-mcp
metadata:
  {
    "openclaw":
      {
        "emoji": "⛓",
        "requires": { "bins": ["uv"] },
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# bitcoin-mcp

Give your AI agent Bitcoin superpowers. 47 tools including fee intelligence, mempool analysis, address lookups, transaction decoding, block inspection, and PSBT security analysis.

Backed by the [Satoshi API](https://bitcoinsapi.com). **Zero config** — works out of the box with no Bitcoin node, no API key.

## Install as MCP server in OpenClaw

Add to your `openclaw.json`:

```json
"mcpServers": {
  "bitcoin": {
    "command": "uvx",
    "args": ["bitcoin-mcp"]
  }
}
```

## Install for Claude Code

```bash
claude mcp add bitcoin -- uvx bitcoin-mcp
```

## Install for Claude Desktop / Cursor

```json
{
  "mcpServers": {
    "bitcoin": {
      "command": "uvx",
      "args": ["bitcoin-mcp"]
    }
  }
}
```

## What you can do

- **Fees:** Real-time fee recommendations, smart fee estimation, cost calculator
- **Mempool:** Pending transactions, ancestors, entry lookup
- **Blocks:** Block stats, comparisons, chain tips
- **Addresses:** Balance, UTXO set, transaction history
- **Transactions:** Decode raw tx, analyze, find inscriptions
- **PSBT:** Security analysis for partially signed transactions
- **Lightning:** Decode BOLT11 invoices
- **Mining:** Pool rankings, difficulty adjustment, halving countdown
- **Market:** Price, supply info, market sentiment

## Links

- PyPI: [bitcoin-mcp](https://pypi.org/project/bitcoin-mcp/)
- GitHub: [Bortlesboat/bitcoin-mcp](https://github.com/Bortlesboat/bitcoin-mcp)
- API docs: [bitcoinsapi.com](https://bitcoinsapi.com)
