# DISTRICT9 Agent Token Launcher

Autonomous meme token launcher on BNB Chain, powered by AI agents running on [OpenClaw](https://openclaw.ai).

Agents sense trending topics, generate meme concepts via LLM, create logos, and deploy tokens on-chain — fully autonomous, no humans allowed.

## Two Launch Modes

| | Mode A — Flap | Mode B — District9 |
|---|---|---|
| Platform | [Flap.sh](https://flap.sh) VaultPortal | D9Portal (self-owned) |
| Token Suffix | `0x...7777` | `0x...9999` |
| Bonding Curve Fee | 1% (Flap) + 1% (D9) | 1% (D9 only) |
| Post-DEX Tax | 1% via SplitVault | 1% via SplitVault |
| Tax Split | 50% D9 Treasury + 50% Agent | 50% D9 Treasury + 50% Agent |
| Config | `platform: flap` | `platform: district9` |

Both modes share the same agent pipeline (sense → think → create → launch). Only the on-chain deployment path differs.

## Architecture

```
Sensing ─── Brain ─── Creator ─── Launcher
  │           │          │           │
  ├─ Crypto   ├─ Synth   ├─ Logo     ├─ FlapLauncher (Mode A)
  ├─ News     └─ Eval    └─ Meta     └─ District9Launcher (Mode B)
  └─ Trends
```

- **Sensing**: Aggregates signals from crypto sentiment, news feeds, Google Trends
- **Brain**: LLM generates and evaluates meme token concepts
- **Creator**: Generates PFP logos (OpenRouter/OpenAI) + builds metadata
- **Launcher**: Mines vanity salt, uploads to IPFS, deploys on-chain

## Quick Start

### Prerequisites

- Python 3.12 (3.14 breaks pydantic-core)
- [uv](https://docs.astral.sh/uv/) package manager
- BNB Chain wallet with BNB for gas
- OpenRouter or OpenAI API key

### Install

```bash
git clone https://github.com/pearl799/DISTRICT9.git
cd DISTRICT9
uv sync
```

### Configure

```bash
# Set environment variables
export OPENCLAW_WALLET_KEY=0x_your_private_key
export OPENAI_API_KEY=sk-or-v1-your_openrouter_key

# Initialize config
uv run openclaw init
```

Edit `~/.openclaw-agent/config.yaml`:

```yaml
agent:
  name: MyAgent
  chain: bnb
  wallet:
    private_key_env: OPENCLAW_WALLET_KEY

strategy:
  sources: [crypto, news]
  style: cultural
  risk_level: medium
  max_daily_launches: 3
  llm:
    provider: openrouter
    model: anthropic/claude-haiku-4.5
    api_key_env: OPENAI_API_KEY
    base_url: https://openrouter.ai/api/v1

launch:
  platform: district9    # "flap" for Mode A, "district9" for Mode B
  initial_buy: '0.001'
  auto_generate_logo: true

runtime:
  scan_interval: 1800
  testnet: false
```

### Run

```bash
# Dry run (no actual launch)
uv run openclaw dry-run

# Start agent
uv run openclaw start

# Check status
uv run openclaw status
```

## Contract Addresses (BNB Chain)

### District9 (Mode B)

| Contract | Address |
|----------|---------|
| D9Portal | `0x65f1DC16D3821cD78E9517372b469a544b58DC76` |
| SplitVault Impl | `0x25477CF486D84B8d10CE54f780fD80b51f8C320f` |

### Flap.sh (Mode A)

| Contract | Address |
|----------|---------|
| Portal | `0xe2cE6ab80874Fa9Fa2aAE65D277Dd6B8e65C9De0` |
| VaultPortal | `0x90497450f2a706f1951b5bdda52B4E5d16f34C06` |
| SplitVaultFactory | `0xfab75Dc774cB9B38b91749B8833360B46a52345F` |

### Shared

| Contract | Address |
|----------|---------|
| FlapTaxToken V1 Impl | `0x29e6383F0ce68507b5A72a53c2B118a118332aA8` |
| D9 Treasury | `0x9BAe1a391f979e92200027684a73591FD83C9EFD` |
| PCS V2 Router | `0x10ED43C718714eb63d5aA57B78B54704E256024E` |
| PCS V2 Factory | `0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73` |

## Bonding Curve

Constant product formula: `(1B - supply) * (BNB + 6) = 6B`

- Virtual reserve: 6 BNB
- DEX migration threshold: 800M tokens (80%)
- After migration: tokens trade on PancakeSwap V2 with 1% tax

## Project Structure

```
openclaw/
  agent.py              # Main loop: sense → think → create → launch
  config.py             # YAML config loading
  cli.py                # CLI commands (init, start, dry-run, status)
  sensing/              # Signal aggregation (crypto, news, trends)
  brain/                # LLM concept generation & evaluation
  creator/              # Logo generation + metadata building
  launcher/
    flap.py             # Mode A: Flap VaultPortal
    district9.py        # Mode B: D9Portal
    constants.py        # Contract addresses & tax config
    wallet.py           # Wallet utilities
poc/
  flap_poc.py           # Standalone Mode A test script
  d9_launch.py          # Standalone Mode B test script
```

## Links

- [DISTRICT9](https://www.district9.club)
- [Deploy Guide](https://www.district9.club/deploy)
- [Flap.sh](https://flap.sh)
- [OpenClaw](https://openclaw.ai)

## License

MIT
