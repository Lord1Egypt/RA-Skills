# eolas-openclaw-mcp

> Trade perps and post to social — all from one AI conversation.

OpenClaw plugin that bridges **EOLAS Edge** (on-chain perpetual trading via Orderly Network) and **EOLAS Reach** (X/Twitter + Telegram + image generation) into native agent tools.

Once installed, just talk to your OpenClaw agent:

> *"Long ETH with $20, 3% stop loss, 6% take profit"* → executes on-chain  
> *"Post this trade to Telegram"* → done  
> *"Scan for the best opportunity right now"* → screens all markets  

No switching tabs. No copying addresses. One conversation.

---

## Install

```bash
openclaw plugins install eolas-openclaw-mcp
```

Then restart your gateway:

```bash
openclaw gateway restart
```

---

## Configuration

Add to your `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "allow": ["eolas-openclaw-mcp"],
    "entries": {
      "eolas-openclaw-mcp": {
        "enabled": true,
        "config": {
          "telegramBotToken": "your-telegram-bot-token",
          "creatorBidApiKey": "your-creatorbid-key",
          "replicateApiToken": "your-replicate-token"
        }
      }
    }
  },
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "allow": ["eolas-openclaw-mcp"]
        }
      }
    ]
  }
}
```

All config keys are optional — only add what you need:

| Key | Required for |
|---|---|
| `telegramBotToken` | Telegram messaging |
| `creatorBidApiKey` | X/Twitter posting |
| `replicateApiToken` | Image & video generation |

---

## Prerequisites

Install the EOLAS MCP servers globally:

```bash
npm install -g eolas-edge-mcp eolas-reach-mcp
```

> **Note:** Requires `eolas-edge-mcp >= 2.0.2` for Node v20+ compatibility.  
> If on an older version, run: `npm install -g eolas-edge-mcp@latest`

---

## What You Get

### Trading Tools (EolasEdge → Orderly Network, Base mainnet)

| Tool | What it does |
|---|---|
| `eolas_get_markets` | List all perp markets |
| `eolas_get_market_info` | Price, funding rate, OI for a symbol |
| `eolas_get_account_balance` | Your USDC balance |
| `eolas_get_positions` | Open positions |
| `eolas_get_orders` | Order history |
| `eolas_get_tradingview_candles` | OHLCV candle data |
| `eolas_place_order` | Market / limit / stop order |
| `eolas_place_bracket_order` | Order with TP + SL attached |
| `eolas_cancel_order` | Cancel by order ID |
| `eolas_close_all_positions` | Emergency close everything |
| `eolas_manage_funds` | Deposit / withdraw USDC |
| `eolas_screen_assets` | Scan markets for opportunities |
| `eolas_swap_token_on_uniswap` | Swap tokens on Uniswap (Base) |

### Social Tools (EolasReach)

| Tool | What it does |
|---|---|
| `eolas_create_twitter_post` | Post a tweet as the EOLAS agent |
| `eolas_reply_to_twitter_post` | Reply to a tweet |
| `eolas_get_twitter_mentions` | Read @mentions |
| `eolas_send_telegram_message` | Send to Telegram |
| `eolas_get_telegram_updates` | Read Telegram messages |
| `eolas_generate_image` | Generate image via Replicate |
| `eolas_generate_brand_image` | EOLAS-branded image |
| `eolas_generate_seedance_video` | Generate video |

---

## Quick Start

**1. Fund your trading wallet**

Ask your agent: *"What is my trading wallet address?"*  
Send USDC (Base network) to that address.

**2. Deposit to Orderly**

> *"Deposit $20 to my Orderly account"*

**3. Trade**

> *"Long BTC with $15, 3% stop loss"*  
> *"Show my open positions"*  
> *"Close everything"*

**4. Post about it**

> *"Send a Telegram message: EOLAS just longed BTC at $X"*

---

## How It Works

The plugin spawns `eolas-edge-mcp` and `eolas-reach-mcp` as child processes when the OpenClaw gateway starts. It communicates with them via the MCP stdio protocol, discovers all available tools, and registers each one as a native OpenClaw agent tool. Credentials are stored in `~/.openclaw/eolas/keychain.json`.

---

## Links

- [EOLAS DEX](https://perps.eolas.fun) — trade directly
- [EOLAS Docs](https://eolas.gitbook.io/eolas) — full documentation
- [OpenClaw](https://openclaw.ai) — AI agent platform
- [ClawHub](https://clawhub.ai) — OpenClaw plugin registry

---

## License

MIT
