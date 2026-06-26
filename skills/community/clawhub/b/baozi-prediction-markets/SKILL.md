--- 
name: baozi-prediction-markets 
description: Access Solana prediction markets on Baozi. Use when user wants to check market odds, get betting quotes, list active markets, analyze opportunities, or place bets. 
version: 1.0.0 
license: MIT 
--- 
 
# Baozi Prediction Markets Skill 
 
## When to Use This Skill 
 
Trigger this skill when the user asks about: 
- "prediction markets on Solana" 
- "Baozi odds" or "betting on [event]" 
- "list active markets" 
- "what are the odds for BTC" 
- "check my positions" 
- "place a bet on [outcome]" 
 
## Protocol Information 
 
**Program ID:** `FWyTPzm5cfJwRKzfkscxozatSxF6Qu78JQovQUwKPruJ` (Baozi Markets V4.7.6) 
**REST API:** https://baozi.bet/api/ 
**MCP Server:** @baozi.bet/mcp-server -- provides 76 pre-built tools 
 
### Market Layers 
 
| Layer | Fee | Who Can Create | Resolution | 
|-------|-----|-----------------|------------| 
| Official | 2.5%% | Admin only | Grandma Mei (AI oracle) | 
| Lab | 3%% | Anyone | Creator OR Council | 
| Private | 2%% | Invite only | Creator OR Council | 
 
## Available Tools 
 
### 1. List Active Markets 
 
To list all active boolean markets: 
 
```bash 
echo '{\"name\":\"list_markets\",\"arguments\":{\"layer\":\"Lab\",\"status\":\"Active\"}}' | npx @baozi.bet/mcp-server 
``` 
 
For race markets (multi-outcome): 
 
```bash 
echo '{\"name\":\"list_race_markets\",\"arguments\":{\"layer\":\"Lab\",\"status\":\"Active\"}}' | npx @baozi.bet/mcp-server 
``` 
 
### 2. Get Market Details 
 
```bash 
echo '{\"name\":\"get_market\",\"arguments\":{\"market\":\"MARKET_PUBKEY\"}}' | npx @baozi.bet/mcp-server 
``` 
 
### 3. Get Betting Quote 
 
```bash 
echo '{\"name\":\"get_quote\",\"arguments\":{\"market\":\"MARKET_PUBKEY\",\"side\":\"Yes\",\"amount\":1.0}}' | npx @baozi.bet/mcp-server 
``` 
 
### 4. Check Wallet Positions 
 
```bash 
echo '{\"name\":\"get_positions\",\"arguments\":{\"wallet\":\"WALLET_ADDRESS\"}}' | npx @baozi.bet/mcp-server 
``` 
 
### 5. Analyze Market 
 
```bash 
echo '{\"name\":\"analyze-market\",\"arguments\":{\"market\":\"MARKET_PUBKEY\"}}' | npx @baozi.bet/mcp-server 
``` 
 
## Security Notes 
 
- **Agent builds transactions, user signs them** -- No private keys in the agent 
- Test on devnet first using free SOL from faucets 
- Enable betting by setting `BAOZI_LIVE=1` environment variable 
- Minimum bet: 0.01 SOL 
- Maximum bet: 100 SOL per transaction 
 
## Affiliate System 
 
On first use, the skill automatically checks if your wallet has an affiliate code registered. 
If not, it registers one automatically using your wallet address as the code. 
 
## Error Handling 
 
Clear error messages for: 
- Invalid market ID 
- Insufficient SOL balance 
- Market closed 
- Bet amount below minimum (0.01 SOL) 
- Bet amount above maximum (100 SOL) 
