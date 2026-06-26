---
name: district9
description: Autonomous meme token launcher on BNB Chain — sense trends, generate concepts, create logos, deploy tokens on-chain
homepage: https://www.district9.club
metadata:
  {
    "openclaw":
      {
        "emoji": "9️⃣",
        "requires":
          {
            "bins": ["uv"],
            "env": ["OPENCLAW_WALLET_KEY"],
          },
        "primaryEnv": "OPENCLAW_WALLET_KEY",
      },
  }
---

# DISTRICT9 Agent Token Launcher

Autonomous meme token launcher on BNB Chain. Agents sense trending topics, generate meme concepts via LLM, create logos, and deploy tokens on-chain.

## Requirements

- Python 3.12 (`uv` managed)
- BNB Chain wallet with BNB for gas
- OpenRouter or OpenAI API key

## Setup

```bash
cd {baseDir}
uv sync
```

Set environment variables:

```bash
export OPENCLAW_WALLET_KEY=0x_your_private_key
export OPENAI_API_KEY=sk-or-v1-your_openrouter_key
```

Initialize config:

```bash
cd {baseDir} && uv run openclaw init
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
  platform: district9
  initial_buy: '0.001'
  auto_generate_logo: true

runtime:
  scan_interval: 1800
  testnet: false
```

## Commands

Use the exec tool, NOT the browser tool, to run these commands.

### Dry Run (no actual launch)

```bash
cd {baseDir} && uv run openclaw dry-run
```

### Start Agent

```bash
cd {baseDir} && uv run openclaw start
```

### Check Status

```bash
cd {baseDir} && uv run openclaw status
```

## Two Launch Modes

| | Mode A — Flap | Mode B — District9 |
|---|---|---|
| Platform | Flap.sh VaultPortal | D9Portal (self-owned) |
| Token Suffix | `0x...7777` | `0x...9999` |
| Bonding Curve Fee | 1% (Flap) + 1% (D9) | 1% (D9 only) |
| Post-DEX Tax | 1% via SplitVault | 1% via SplitVault |
| Config | `platform: flap` | `platform: district9` |

Set `launch.platform` in config to switch modes.

## Architecture

```
Sensing --> Brain --> Creator --> Launcher
  |           |          |           |
  +- Crypto   +- Synth   +- Logo     +- FlapLauncher (Mode A)
  +- News     +- Eval    +- Meta     +- District9Launcher (Mode B)
  +- Trends
```

## Contract Addresses (BNB Chain)

- D9Portal: `0x65f1DC16D3821cD78E9517372b469a544b58DC76`
- SplitVault Impl: `0x25477CF486D84B8d10CE54f780fD80b51f8C320f`
- D9 Treasury: `0x9BAe1a391f979e92200027684a73591FD83C9EFD`

## Links

- [DISTRICT9](https://www.district9.club)
- [GitHub](https://github.com/pearl799/DISTRICT9)
