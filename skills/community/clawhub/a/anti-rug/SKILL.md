---
name: anti-rug-cn
version: 3.1.0
description: "Web3 token security scanner with expert cross-validation engine. Detects honeypots, rug pulls, and contract risks across Ethereum, BSC, Polygon, and other EVM chains."
author: Antalpha AI Team
requires: [python>=3.8, requests>=2.28.0]
metadata:
  repository: https://github.com/ZorroShao/anti-rug
  install:
    type: python
    command: pip install -r requirements.txt
  env: []
---

# Web3 Token Security Scanner (Anti-Rug)

**Maintainer: Antalpha AI Team**

A professional-grade token contract security analyzer featuring scenario-based classification and cross-validation engine.

## Overview

This tool performs comprehensive security analysis of token contracts with:
- **Scenario Classification**: Automatically categorizes tokens (A: Pegged Assets, B: Eco Tokens, C: Meme Coins)
- **Cross-Validation Engine**: Analyzes relationships between indicators (neutralized/amplified/contextual)
- **Dynamic Risk Scoring**: Weighted scoring system adapted to token type
- **Fatal Finding Detection**: One-strike rules for critical vulnerabilities

## Supported Chains

- Ethereum (chain_id: 1)
- BNB Smart Chain (chain_id: 56)
- Polygon (chain_id: 137)
- Arbitrum One (chain_id: 42161)
- Base (chain_id: 8453)
- Optimism (chain_id: 10)
- Avalanche C-Chain (chain_id: 43114)
- Solana (chain_id: solana)

## Installation

```bash
git clone https://github.com/ZorroShao/anti-rug.git
cd anti-rug
pip install -r requirements.txt
```

## Usage

```bash
python scripts/check_token.py --chain_id 56 --contract_address 0x...
```

## Scenario Classification

### Scenario A: Pegged/Stable Assets
Examples: USDT, USDC, WETH, WBNB
- Mintable: ✅ Expected for peg maintenance
- Owner: ✅ Institution custody is normal
- Blacklist: ✅ Compliance requirement

### Scenario B: Ecosystem Tokens
Examples: UNI, AAVE, established DeFi
- Proxy: ✅ Acceptable for upgradeability
- Treasury: ✅ Protocol-owned liquidity expected

### Scenario C: Meme/Unknown Tokens
- All permissions: ⚠️ Treated as potential rug tools
- Strictest evaluation applied

## Risk Severity Levels

| Score | Level | Action |
|-------|-------|--------|
| 0-24 | Low | ✅ Base security passed |
| 25-49 | Low-Medium | 🟡 Minor concerns |
| 50-74 | Medium | 🟡 Caution required |
| 75-100 | High | 🔴 Dangerous |
| Fatal | Critical | 🛑 Do not buy |

## Architecture

```
config.py           # Centralized configuration
exceptions.py       # Custom exception classes
validators/         # Cross-validation rules (modular)
  cv_mint_ownership.py
  cv_concentration.py
  cv_proxy.py
  cv_tax_scenario.py
tests/              # Unit tests
scripts/
  check_token.py    # Main entry point
```

## License

MIT License - See LICENSE file
