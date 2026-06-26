---
name: eolas
description: Trade perpetual futures and send social updates via EOLAS DEX. Place and manage orders on Orderly Network, post updates to Telegram or X/Twitter.
metadata: {"openclaw":{"requires":{"config":["plugins.entries.eolas-openclaw-mcp.enabled"]},"install":[{"id":"node","kind":"node","package":"eolas-openclaw-mcp","label":"Install EOLAS MCP plugin"}]}}
---

# EOLAS Skill

Connect your OpenClaw agent to the EOLAS perpetuals exchange (perps.eolas.fun) and social tools.

## Setup

**1. Install the EOLAS MCP servers (required):**
```bash
npm install -g eolas-edge-mcp eolas-reach-mcp
```

**2. Install this plugin:**
```bash
openclaw plugins install eolas-openclaw-mcp
```

**3. Add to `~/.openclaw/openclaw.json`:**
```json
{
  "plugins": {
    "allow": ["eolas-openclaw-mcp"],
    "entries": {
      "eolas-openclaw-mcp": {
        "enabled": true,
        "config": {
          "telegramBotToken": "optional - for Telegram messaging",
          "creatorBidApiKey": "optional - for X/Twitter posting",
          "replicateApiToken": "optional - for image generation"
        }
      }
    }
  }
}
```

All config keys are **optional** — only add what you need. No keys are stored in code; they live in your local OpenClaw config only.

**Credential storage:** Trading account credentials are stored locally at `~/.openclaw/eolas/keychain.json` on first use. No credentials are sent anywhere except to the EOLAS API (`api.orderly.org`).

## Trading

- "What markets are available on EOLAS?"
- "Show me the BTC funding rate"
- "Long ETH with $20, 3% stop loss, 6% take profit"
- "Show my open positions"
- "Close my BTC position"
- "What is my account balance?"
- "Scan markets for the best opportunity"

## Social

- "Send a Telegram message: BTC just hit $X"
- "Post a tweet about this trade"
- "Get my latest Twitter mentions"
- "Generate an image for this signal"

## Tools

**Trading (13 tools via EOLAS Edge → Orderly Network, Base mainnet)**

- `eolas_get_markets` — list all markets
- `eolas_get_market_info` — price, funding rate, open interest
- `eolas_get_account_balance` — account balance
- `eolas_get_positions` — open positions
- `eolas_get_orders` — order history
- `eolas_get_tradingview_candles` — OHLCV data
- `eolas_place_order` — market or limit order
- `eolas_place_bracket_order` — order with take profit + stop loss
- `eolas_cancel_order` — cancel an order
- `eolas_close_all_positions` — close all positions
- `eolas_manage_funds` — deposit or withdraw USDC
- `eolas_screen_assets` — scan markets for setups
- `eolas_swap_token_on_uniswap` — swap tokens on Base

**Social (16 tools via EOLAS Reach)**

- `eolas_send_telegram_message` — send to Telegram
- `eolas_get_telegram_updates` — read Telegram messages
- `eolas_create_twitter_post` — post on X/Twitter
- `eolas_reply_to_twitter_post` — reply to a tweet
- `eolas_get_twitter_mentions` — read mentions
- `eolas_generate_image` — generate image via Replicate
- `eolas_generate_brand_image` — EOLAS branded image
- `eolas_generate_seedance_video` — generate video
- `eolas_merge_videos` — merge video clips
- `eolas_add_reference_image` — add reference image
- `eolas_list_reference_images` — list reference images
- `eolas_add_brand_template` — add brand template
- `eolas_list_brand_templates` — list brand templates
- `eolas_delete_brand_template` — delete brand template
- `eolas_list_available_fonts` — list fonts
- `eolas_generate_nano_banana_image` — nano banana image

## Links

- EOLAS DEX: https://perps.eolas.fun
- Plugin on npm: https://npmjs.com/package/eolas-openclaw-mcp
- EOLAS Docs: https://eolas.gitbook.io/eolas
- Source: https://github.com/Albertech2005/eolas-openclaw-mcp
