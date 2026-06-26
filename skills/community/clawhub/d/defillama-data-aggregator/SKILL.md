---
name: defillama-data-aggregator
description: Professional DeFi data aggregator that provides unified access to TVL, protocols, chains, and yields data from DefiLlama. Supports multiple output formats (JSON/Table/CSV), health monitoring, and security validation.
homepage: https://github.com/AntalphaAI/defillama-data-aggregator
version: 1.0.3
author: AntalphaAI
emoji: "📊"
tags: defi,web3,crypto,tvl,data,blockchain,yields,defillama
metadata:
  openclaw:
    requires:
      bins: ["node", "npm"]
      env: []
    install:
      command: "npm install"
  repository: https://github.com/AntalphaAI/defillama-data-aggregator
---

# DefiLlama Data Aggregator

> **Professional DeFi data at your fingertips.** Query TVL, protocols, chains, and yields from DefiLlama with a single command.

## What This Skill Does

- **TVL Query** - Get total DeFi TVL or individual chain TVL
- **Protocol Data** - Query protocol details, rankings, and filter by category
- **Chain Statistics** - Get TVL for specific chains (Ethereum, Solana, etc.)
- **Yield Pools** - Find high-yield opportunities with filtering options
- **Health Monitoring** - Check API availability status

## Quick Start

```bash
# Get total DeFi TVL
node {skillDir}/src/index.js defillama tvl

# Get protocol TVL
node {skillDir}/src/index.js defillama protocol --name aave

# Get top protocols by TVL
node {skillDir}/src/index.js defillama protocols --limit 10 --sort tvl --format table

# Get chain TVL
node {skillDir}/src/index.js defillama chain --name ethereum

# Find high-yield pools
node {skillDir}/src/index.js defillama yields --min-apy 10 --chain ethereum --limit 20

# Check API health
node {skillDir}/src/index.js health
```

## Commands

### TVL Commands

| Command | Description | Example |
|---------|-------------|---------|
| `tvl` | Get total DeFi TVL | `node {skillDir}/src/index.js defillama tvl` |
| `protocol --name <name>` | Get protocol TVL | `node {skillDir}/src/index.js defillama protocol --name uniswap` |
| `chain --name <name>` | Get chain TVL | `node {skillDir}/src/index.js defillama chain --name solana` |

### Protocol Commands

| Command | Description | Example |
|---------|-------------|---------|
| `protocols` | List all protocols | `node {skillDir}/src/index.js defillama protocols` |
| `protocols --category <cat>` | Filter by category | `node {skillDir}/src/index.js defillama protocols --category lending` |
| `protocols --min-tvl <usd>` | Filter by minimum TVL | `node {skillDir}/src/index.js defillama protocols --min-tvl 100000000` |
| `protocols --limit <n>` | Limit results | `node {skillDir}/src/index.js defillama protocols --limit 20` |

### Yield Commands

| Command | Description | Example |
|---------|-------------|---------|
| `yields` | List yield pools | `node {skillDir}/src/index.js defillama yields` |
| `yields --min-apy <pct>` | Filter by minimum APY | `node {skillDir}/src/index.js defillama yields --min-apy 15` |
| `yields --chain <name>` | Filter by chain | `node {skillDir}/src/index.js defillama yields --chain arbitrum` |
| `yields --min-tvl <usd>` | Filter by minimum TVL | `node {skillDir}/src/index.js defillama yields --min-tvl 1000000` |
| `yields --stablecoin` | Stablecoin pools only | `node {skillDir}/src/index.js defillama yields --stablecoin` |

### Utility Commands

| Command | Description | Example |
|---------|-------------|---------|
| `health` | Check API health | `node {skillDir}/src/index.js health` |
| `status` | Show system status | `node {skillDir}/src/index.js status` |

## Output Formats

All data commands support multiple output formats:

```bash
# Pretty format (default, human-readable)
node {skillDir}/src/index.js defillama tvl --format pretty

# JSON format (for scripts and parsing)
node {skillDir}/src/index.js defillama tvl --format json

# Table format (for quick overview)
node {skillDir}/src/index.js defillama protocols --limit 10 --format table

# CSV format (for spreadsheets)
node {skillDir}/src/index.js defillama protocols --limit 50 --format csv
```

## Use Cases

### For DeFi Investors
```
"Show me the top 10 lending protocols by TVL"
"Find yield pools on Ethereum with APY above 15%"
"What is the current TVL of Aave?"
```

### For Data Analysts
```
"Export all protocols data to CSV"
"Get the TVL distribution across chains"
"Compare lending vs DEX TVL"
```

### For Developers
```
"Check if DefiLlama API is healthy"
"Get protocol data in JSON format"
"Find pools with minimum 1M TVL"
```

## Security Features

- **Input Sanitization** - All inputs validated and sanitized
- **Error Filtering** - API errors filtered to prevent information leakage
- **Range Validation** - Numeric inputs validated against bounds
- **Pattern Validation** - Protocol/chain names follow strict rules

## Security Notes

- **No API Keys Required**: This skill uses DefiLlama's public API which does not require authentication
- **External Requests**: Data is fetched from:
  - `https://api.llama.fi` (DefiLlama API)
  - `https://yields.llama.fi` (DefiLlama Yields API)
- **No Local Server**: This skill does not start any local HTTP server
- **No File Persistence**: No data is persisted locally (caching is in-memory only)
- **Input Validation**: All user inputs are sanitized to prevent injection attacks

## Installation

### Prerequisites
- Node.js >= 16.0.0
- npm

### Setup
```bash
cd {skillDir}
npm install
```

## API Reference

### DefiLlama Endpoints Used

| Endpoint | Description |
|----------|-------------|
| `https://api.llama.fi/tvl` | Total DeFi TVL |
| `https://api.llama.fi/protocols` | All protocols |
| `https://api.llama.fi/protocol/{name}` | Protocol details |
| `https://api.llama.fi/chains` | All chains |
| `https://yields.llama.fi/pools` | Yield pools |

## Error Handling

The skill provides user-friendly error messages:

| Error Type | Message |
|------------|---------|
| Invalid protocol name | "Only alphanumeric characters and hyphens allowed" |
| Invalid chain name | "Only alphanumeric characters, spaces, and hyphens allowed" |
| Network error | "Check internet connection and try again" |
| Rate limit | "Rate limit exceeded, please wait" |
| API unavailable | "Service temporarily unavailable" |

## Examples

### Get Top Protocols
```bash
node {skillDir}/src/index.js defillama protocols --limit 10 --sort tvl --format table
```

### Find High-Yield Pools
```bash
node {skillDir}/src/index.js defillama yields --min-apy 20 --min-tvl 1000000 --limit 5
```

### Check Health
```bash
node {skillDir}/src/index.js health
```

## Troubleshooting

### Protocol Not Found
- Ensure the protocol name matches DefiLlama's naming (e.g., `aave-v3` not `aave v3`)
- Check if the protocol is listed on DefiLlama

### Chain Not Found
- Use lowercase chain names (e.g., `ethereum` not `Ethereum`)
- For multi-word chains, use hyphens (e.g., `polygon-pos`)

### No Results from Yields
- Try lowering the `--min-apy` or `--min-tvl` thresholds
- Ensure the chain name is valid

### Network Errors
- Check internet connectivity
- DefiLlama API may be temporarily unavailable

---

**Version**: 1.0.3  
**Last Updated**: 2026-03-31  
**Maintainer**: AntalphaAI  
**License**: MIT
