# Anti-Rug Token Security Checker

**Maintainer: Antalpha AI Team**

A professional-grade Web3 token contract security analyzer featuring scenario-based classification and cross-validation engine.

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
git clone https://github.com/AntalphaAI/anti-rug.git
cd anti-rug
pip install -r requirements.txt
```

## Usage

```bash
python scripts/check_token.py --chain_id 56 --contract_address 0x...
```

### With Custom API Gateway

```bash
python scripts/check_token.py --chain_id 56 --contract_address 0x... --api_gateway https://your-proxy.com
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
anti-rug/
├── config.py           # Centralized configuration
├── exceptions.py       # Custom exception classes
├── requirements.txt    # Dependencies
├── scripts/
│   └── check_token.py  # Main entry point
├── validators/         # Cross-validation rules (modular)
│   ├── cv_mint_ownership.py
│   ├── cv_concentration.py
│   ├── cv_proxy.py
│   └── cv_tax_scenario.py
└── tests/              # Unit tests
    └── test_anti_rug.py
```

## Key Features

### 1. Cross-Validation Engine
Instead of listing raw indicators, the tool analyzes relationships:
- **Neutralized**: Risk is mitigated (e.g., mintable but owner is dead)
- **Amplified**: Risks compound (e.g., high tax + meme coin)
- **Contextual**: Explained by context (e.g., DEX pools in concentration)

### 2. Rule-Based Fatal Detection
Critical vulnerabilities trigger immediate warnings:
- Honeypot (cannot sell)
- Self-destruct function
- Hidden owner
- Extreme sell tax (>50%)

### 3. Scenario-Aware Scoring
Different weights for different token types:
- Pegged assets: Focus on taxes and honeypot
- Ecosystem tokens: Balanced evaluation
- Meme coins: Strict scrutiny of all permissions

## Example Output

```json
{
  "scenario_classification": {
    "scenario": "B",
    "label": "Ecosystem Token / DeFi / GameFi"
  },
  "risk_score": {
    "final_score": 27.0,
    "dimension_scores": {
      "contract_security": 0,
      "tax_risk": 0,
      "liquidity_risk": 0,
      "concentration_risk": 80
    }
  },
  "final_verdict": {
    "risk_level": "LOW_MEDIUM",
    "verdict": "🟡 Minor risk. Research team background before investing."
  }
}
```

## Testing

```bash
python -m pytest tests/
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

MIT License - See [LICENSE](LICENSE) file

## Disclaimer

This tool analyzes on-chain contract security only and does not constitute investment advice. Contract safety ≠ project value. Always conduct your own research on team background, liquidity, and market conditions.

---

**Maintainer**: Antalpha AI Team  
**Repository**: https://github.com/AntalphaAI/anti-rug
