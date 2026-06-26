---
name: antalpha-ai-setup
description: Install and configure the Antalpha Skills MCP server. Provides 146+ Web3 tools for DEX swaps, smart money tracking, Polymarket prediction markets, Hyperliquid perpetuals, CEX trading, Bitcoin mining, and DeFi analytics.
version: 2.0.0
author: Antalpha Labs
homepage: https://mcp-skills.ai.antalpha.com
---

# Antalpha Skills MCP Server Setup

## Overview
The Antalpha Skills MCP server provides 146+ Web3 tools for AI agents, including DEX swaps, smart money tracking, Polymarket prediction markets, Hyperliquid perpetuals, CEX trading, Bitcoin mining, and DeFi analytics. This server enables AI agents to interact with various Web3 protocols through a unified Model Context Protocol (MCP) interface.

## Quick Install
```bash
mcporter add https://mcp-skills.ai.antalpha.com/mcp --name antalpha-skills
```

## Prerequisites
- An AI agent capable of using Model Context Protocol (MCP) servers
- Access to the Antalpha Skills MCP server at `https://mcp-skills.ai.antalpha.com/mcp`
- Agent registration with Antalpha (contact team for access)

## Step 1: Add MCP Server
Add the Antalpha Skills server to your MCP-compatible client:

### Claude.ai / Claude Code
1. Go to Settings → Integrations
2. Click "Add Integration"
3. Enter URL: `https://mcp-skills.ai.antalpha.com/mcp`
4. Follow authentication prompts

### Codex
1. Open Codex settings
2. Navigate to "External Services"
3. Add new service with URL: `https://mcp-skills.ai.antalpha.com/mcp`

### Claude Desktop/Cursor/Windsurf
1. Access MCP integrations panel
2. Select "Add New Server"
3. Enter: `https://mcp-skills.ai.antalpha.com/mcp`

### Gemini CLI
1. Configure MCP endpoints
2. Add: `https://mcp-skills.ai.antalpha.com/mcp`

### OpenCode
1. In settings, find "MCP Servers"
2. Add the Antalpha endpoint

### OpenClaw
Edit your OpenClaw configuration to include:
```json
{
  "mcpServers": [
    {
      "name": "antalpha-skills",
      "url": "https://mcp-skills.ai.antalpha.com/mcp",
      "enabled": true
    }
  ]
}
```

Note: For OpenClaw, use the direct HTTP URL rather than the npx mcp-remote command.

## Step 2: Register Your Agent
Contact the Antalpha team to register your AI agent. You'll need to provide:
- Agent name and description
- Intended use case
- Expected request volume
- Contact information for support

Upon registration, you'll receive agent-specific credentials and rate limits.

## Step 3: Verify Installation
Test your installation by running the ping command:

```bash
# If using the test tool directly
test-ping
```

This should return a simple confirmation that your agent can communicate with the Antalpha Skills server.

## Step 4: Get Your First Result
Try one of these example prompts to verify functionality:

| Prompt | Expected Result |
|--------|----------------|
| "Get current BTC and ETH prices" | Returns latest price data for both cryptocurrencies |
| "Check wallet balance for 0x&lt;your_wallet_address&gt;" | Shows token balances for the specified address |
| "Show trending airdrops" | Lists current airdrop opportunities |
| "Get Hyperliquid account info for address" | Retrieves account details from Hyperliquid |

## Available Tools
| Tool | Description |
|------|-------------|
| swap-quote | Get quotes for token swaps across multiple chains |
| swap-create-page | Create swap transaction pages for user approval |
| swap-tokens | Search for available tokens on specific chains |
| swap-gas | Get current gas estimates for swaps |
| swap-full | Execute complete swap transactions |
| smart-swap-create | Create smart swap orders with advanced parameters |
| smart-swap-list | List smart swap orders for a wallet |
| smart-swap-status | Check status of a specific smart swap order |
| smart-swap-cancel | Cancel a smart swap order |
| smart-money-signal | Get smart money signals based on whale activity |
| smart-money-watch | Watch specific addresses for smart money activity |
| smart-money-list | List addresses currently being watched |
| smart-money-custom | Manage custom smart money settings |
| smart-money-scan | Scan for new smart money opportunities |
| smart-money-pool | Monitor liquidity pool activity |
| poly-intel | Get intelligence data about Polymarket traders/markets |
| poly-master-traders | Get top performing traders on Polymarket |
| poly-master-search-market | Search for Polymarket markets |
| poly-master-follow | Follow a Polymarket trader to copy trades |
| poly-master-status | Get status of your Polymarket account |
| poly-master-risk | Manage risk settings for Polymarket trading |
| poly-master-pnl | Get profit and loss data for Polymarket |
| poly-orders | Get list of Polymarket orders |
| poly-trending | Get trending Polymarket markets |
| poly-new | Get newly created Polymarket markets |
| poly-market-info | Get detailed information about a market |
| poly-positions | Get your current Polymarket positions |
| poly-history | Get your Polymarket trade history |
| poly-buy | Buy shares in a Polymarket market |
| poly-sell | Sell shares in a Polymarket market |
| poly-confirm | Confirm a Polymarket order or check status |
| poly-master-strategy-scan | Scan for profitable trading strategies |
| poly-master-strategy-metrics | Get performance metrics for strategies |
| poly-master-strategy-dry-run | Enable/disable dry-run mode for strategies |
| hl-price | Get current price for a coin on Hyperliquid |
| hl-account | Get account information for a Hyperliquid address |
| hl-book | Get the order book for a coin on Hyperliquid |
| hl-orders | Get open orders for a Hyperliquid address |
| hl-positions | Get current positions for a Hyperliquid address |
| hl-funding | Get funding rate information on Hyperliquid |
| hl-balance-check | Check if a trade is possible given account balance |
| hl-limit-order | Place a limit order on Hyperliquid |
| hl-market-order | Place a market order on Hyperliquid |
| hl-close | Close a position on Hyperliquid |
| hl-cancel | Cancel an open order on Hyperliquid |
| hl-leverage | Set leverage for a coin on Hyperliquid |
| hl-tp-sl | Set take profit or stop loss for a position |
| hl-modify-order | Modify an existing order on Hyperliquid |
| cex-account-get-balance | Get account balance from centralized exchange |
| cex-account-get-info | Get detailed account information from CEX |
| cex-futures-place-order | Place a futures order on a CEX |
| cex-futures-cancel-order | Cancel a futures order on a CEX |
| cex-futures-get-positions | Get current futures positions on a CEX |
| cex-futures-set-leverage | Set leverage for a futures position |
| cex-futures-close-position | Close a futures position on a CEX |
| cex-market-get-ticker | Get ticker information for an instrument |
| cex-market-get-kline | Get k-line data for an instrument |
| cex-market-get-orderbook | Get order book for an instrument |
| cex-market-get-instruments | Get list of available instruments on an exchange |
| cex-setup-check | Check if CEX setup is properly configured |
| cex-spot-place-order | Place a spot order on a CEX |
| cex-spot-cancel-order | Cancel a spot order on a CEX |
| cex-spot-get-orders | Get list of spot orders from a CEX |
| macro-fred-cpi | Get Consumer Price Index data from FRED |
| macro-fred-nfp | Get Non-Farm Payrolls data from FRED |
| macro-fred-m2 | Get M2 Money Supply data from FRED |
| macro-fred-yield-spread | Get Treasury Yield Spread data from FRED |
| macro-fred-unemployment | Get Unemployment Rate data from FRED |
| macro-fred-sahm | Get Sahm Rule Recession Indicator from FRED |
| macro-fred-fed-rate | Get Federal Funds Rate data from FRED |
| macro-fred-all | Get all available FRED macro indicators |
| macro-fred-cache-clear | Clear cached FRED data |
| crypto-social-trending | Get trending cryptocurrencies on social media |
| crypto-sentiment-score | Get sentiment score for a cryptocurrency |
| crypto-kol-signals | Get signals from crypto Key Opinion Leaders |
| crypto-mention-surge | Get cryptocurrencies with mention surges |
| crypto-fear-greed | Get the current crypto fear and greed index |
| wallet-guard-token-security | Check security of a token contract |
| wallet-guard-address-security | Check security of a wallet address |
| wallet-guard-approval-security | Check security of wallet approvals |
| wallet-guard-nft-security | Check security of an NFT contract |
| wallet-guard-phishing-site | Check if a URL is a phishing site |
| wallet-guard-token-deep-scan | Perform a deep security scan of a token |
| wallet-guard-rugpull-detection | Detect potential rugpull risks for a token |
| wallet-balance-query | Query wallet balance across multiple chains |
| airdrop-scan | Scan for active airdrops |
| airdrop-daily-report | Get daily airdrop report |
| airdrop-check-project | Check details of an airdrop project |
| airdrop-zero-cost | Find zero-cost airdrops |
| airdrop-scam-check | Check if an airdrop project is a scam |
| easy-mining-get-workspace | Get mining workspace information |
| easy-mining-list-farms | List mining farms in the workspace |
| easy-mining-list-agents | List mining agents in the workspace |
| easy-mining-list-miners | List miners in a specific farm |
| easy-mining-list-metrics-history | Get historical metrics for a farm |
| easy-mining-list-pool-diffs | Get pool difficulty history for a farm |
| easy-mining-list-history | Get historical data for a specific miner |
| easy-mining-list-miner-tasks | Get tasks assigned to a specific miner |
| easy-mining-list-task-batches | Get task batches for a farm |
| easy-mining-create-task-batch | Create a new task batch for a farm |
| easy-mining-get-task-batch | Get details of a specific task batch |
| meme-analyze | Analyze a meme token |
| investor_discover | Discover new DeFi investment opportunities |
| investor_analyze | Analyze a specific DeFi investment product |
| investor_compare | Compare multiple DeFi investment products |
| transfer-request | Request a token transfer between wallets |
| transfer-status | Check the status of a token transfer |
| transfer-cancel | Cancel a pending token transfer |
| web-search-query | Perform a web search using various backends |
| web-search-extract | Extract content from a specific URL |
| test-ping | Test connectivity to the MCP server |
| data-price-btc | Get current BTC price data |
| data-price-eth | Get current ETH price data |
| data-sentiment-fng | Get current crypto fear and greed index |
| data-sentiment-funding-btc | Get BTC funding rate sentiment |
| data-sentiment-futures-premium-btc | Get BTC futures premium sentiment |
| data-sentiment-oi-dex | Get DEX open interest sentiment |
| data-sentiment-stablecoin-mcap | Get stablecoin market cap sentiment |
| data-structure-btc-dominance | Get BTC dominance data |
| data-structure-defi-tvl | Get DeFi TVL data |
| data-structure-defi-tvl-ethereum | Get Ethereum DeFi TVL data |
| data-structure-dex-volume | Get DEX volume data |
| data-structure-eth-btc | Get ETH/BTC ratio data |
| data-whale-etf-flow | Get ETF flow data |
| data-whale-exchange-reserve | Get exchange reserve data |
| data-whale-coinbase-premium | Get Coinbase premium data |
| data-whale-taker-ratio | Get taker ratio data |
| data-vol-oi-cex | Get CEX open interest volatility data |
| data-vol-liquidations | Get liquidation data |
| data-vol-options-max-pain | Get options max pain data |
| data-vol-options-oi | Get options open interest data |
| data-yield-steth | Get stETH yield data |
| data-yield-stablecoin | Get stablecoin yield data |
| data-yield-defi-all | Get overall DeFi yield data |
| data-ta-rsi-btc | Get BTC RSI technical indicator |
| data-ta-ma200 | Get 200-day moving average data |
| data-ta-macd | Get MACD indicator data |
| data-ta-bollinger | Get Bollinger Bands data |
| data-ta-ahr999 | Get AHR999 indicator data |
| data-ta-puell | Get Puell Multiple indicator data |
| data-event-token-unlock | Get token unlock event data |
| data-event-security-alert | Get security alert data |

## Troubleshooting
- If tools aren't appearing in your client, verify the MCP server URL is correctly entered
- For authentication issues, confirm your agent is properly registered with Antalpha
- For rate limiting errors, check with the Antalpha team about adjusting your limits
- If specific tools return errors, check that you're providing all required parameters
- For wallet-related tools, ensure you're using valid wallet addresses
- If experiencing connectivity issues, verify your network connection and firewall settings allow outbound connections to the Antalpha server