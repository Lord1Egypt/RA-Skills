# MCP Servers

Installation reference for CRIF MCP data sources. Read this file only when installing or configuring MCP servers for the user.

---

## coingecko

- **Provider:** CoinGecko (official)
- **Auth:** Demo API key (free), Pro key optional for higher limits
- **Get key:** https://www.coingecko.com/en/api
- **Docs:** https://docs.coingecko.com/docs/mcp-server

**Option A — Remote (no install, rate-limited, no key needed):**
```json
"coingecko": {
  "command": "npx",
  "args": ["-y", "mcp-remote", "https://mcp.api.coingecko.com/mcp"]
}
```

**Option B — Local (recommended, higher limits with key):**
```json
"coingecko": {
  "command": "npx",
  "args": ["-y", "@coingecko/coingecko-mcp"],
  "env": {
    "COINGECKO_DEMO_API_KEY": "your-demo-key-here"
  }
}
```

---

## coinmarketcap

- **Provider:** Shinzo Labs (community)
- **Auth:** API key required (free Basic tier available)
- **Get key:** https://coinmarketcap.com/api/
- **Docs:** https://github.com/shinzo-labs/coinmarketcap-mcp

```json
"coinmarketcap": {
  "command": "npx",
  "args": ["-y", "@shinzolabs/coinmarketcap-mcp"],
  "env": {
    "COINMARKETCAP_API_KEY": "your-key-here",
    "SUBSCRIPTION_LEVEL": "Basic"
  }
}
```

---

## defillama

- **Provider:** IQ AI (community, uses DeFiLlama public API)
- **Auth:** No API key required
- **Docs:** https://github.com/IQAIcom/defillama-mcp

```json
"defillama": {
  "command": "npx",
  "args": ["-y", "@iqai/defillama-mcp"]
}
```

---

## dune

- **Provider:** Community (ekailabs)
- **Auth:** API key required
- **Get key:** https://dune.com/settings/api
- **Docs:** https://github.com/ekailabs/dune-mcp-server

```json
"dune": {
  "command": "npx",
  "args": ["-y", "dune-mcp-server"],
  "env": {
    "DUNE_API_KEY": "your-key-here"
  }
}
```

---

## exa

- **Provider:** Exa (official)
- **Auth:** API key required
- **Get key:** https://exa.ai
- **Docs:** https://github.com/exa-labs/exa-mcp-server

**Option A — Remote:**
```json
"exa": {
  "command": "npx",
  "args": ["-y", "mcp-remote", "https://mcp.exa.ai/mcp?exaApiKey=your-key-here"]
}
```

**Option B — Local (recommended):**
```json
"exa": {
  "command": "npx",
  "args": ["-y", "exa-mcp-server"],
  "env": {
    "EXA_API_KEY": "your-key-here"
  }
}
```
