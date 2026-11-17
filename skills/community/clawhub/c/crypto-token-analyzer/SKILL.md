---
name: crypto-token-analyzer
description: Analyze a cryptocurrency token by contract address and chain. Fetch price, volume, liquidity, price changes, tags, security risks, and trend signals from DexScreener plus block explorers and GoPlus. Give subjective bullish/bearish/uncertain view and position strategy (clear/add/hold if holding; buy/watch if empty). Trigger on contract address+chain, token analysis, 看涨看跌, K线, 策略建议, honeypot check, or similar crypto token queries.
---

# Crypto Token Analyzer

Analyze any token given its contract address and chain. Combine live market data, on-chain signals, and security checks, then give a clear subjective judgment and actionable strategy advice. Always respond in the language of the current conversation.

## Supported Chains (default)

ethereum, bsc, solana, base, arbitrum, polygon, avalanche

- ETH/Ethereum → ethereum
- BSC/BNB → bsc
- SOL → solana
- etc.

## Required workflow

1. **Normalize inputs**
   - Confirm or ask for missing chain if ambiguous.
   - Normalize address (trim, lowercase for EVM; keep case for Solana).

2. **Fetch market data (primary DexScreener)**
   - Prefer API calls via bash + `curl` for speed and reliability.

   ```bash
   curl 'https://api.dexscreener.com/latest/dex/tokens/{tokenAddress}'
   curl 'https://api.dexscreener.com/latest/dex/pairs/v1/{chainId}/{tokenAddress}'
   ```

   - `priceUsd`, `priceChange` (m5/h1/h6/h24), `volume`, `liquidity`, `fdv`, `marketCap`, `pairCreatedAt`, `txs` (buys/sells), `labels`, `info` (socials, websites), `boost`.
   - If multiple pairs, prefer the one with highest liquidity on the requested chain.
   - Open the DexScreener page (`//dexscreener.com/{chain}/{address}`) with browser tools if API fails or richer chart context is needed.

3. **Fetch security & risk (GoPlus + explorers)**
   - GoPlus (free public endpoint, no key required for basic):

   ```bash
   curl 'https://api.gopluslabs.io/api/v1/token_security/{goplusChain_id}?contract_addresses={address}'
   ```

   - ethereum=1, bsc=56, polygon=137, arbitrum=42161, avalanche=43114, base=8453.
   - Solana has limited / different support — note when unavailable.
   - Check: `is_honeypot`, `buy_tax`, `sell_tax`, `is_open_source`, `is_proxy`, `can_take_back_ownership`, `owner_change_balance`, `owner_is_mintable`, `transfer_pausable`, `is_blacklisted`, `lp_holder_count`, `holder_count`, `liquidity_locked` (and if present, `liquidity_locked_info`).
   - EVM: Etherscan / BscScan / Basescan etc. — check contract verification, holder distribution, recent large transfers.
   - Solana: Solscan or Birdeye.
   - Always surface critical risks (honeypot, high tax, mintable, unlocked liquidity, concentrated holders) prominently.
   - **Holder growth & heat normality check** (additional):
     - Use current holder count (GoPlus) plus any historical/trend signals available from explorer pages.
     - DexScreener pair age / volume / txs trajectory or browser inspection.
     - Evaluate recent holder-count / growth rate: extremely rapid spikes (especially on very new pairs) can indicate artificial pumping or hot-stage stegan t; declining holders and rising price/volume can signal weak organic interest.
     - 24h/1h volume, buy/sell ratio, DexScreener boost, social links activity, and overall pair age.
     - Elevated risk when holder growth is disproportionately fast or slow relative to volume and heat, or when heat is high but holder base remains tiny/concentrated.
     - Treat as supporting evidence for the overall risk picture, not a standalone verdict.
     - Note data limitations when historical holder series is unavailable.

4. **K-Line / trend description**
   - From DexScreener `priceChange` + volume + txns describe short-term (5m/1h) and medium-term (6h/24h) momentum.
   - If user asks for visual K-line or deeper chart, open the DexScreener or GeckoTerminal page and describe the visible pattern (or use browser screenshot if available).
   - Note that free APIs do not return full historical OHLC candles; describe relative strength instead.

5. **Subjective judgment**
   - Synthesize price action, volume, liquidity depth, security risks, age of pair, social signals into one clear call: **看涨 / 看跌 / 不确定** (or Bullish / Bearish / Uncertain in English).
   - Be honest about uncertainty — liquidity new pairs, conflicting signals, or high-risk → lean **不确定**.
   - Never claim certainty or guarantee returns.

6. **Strategy advice** (free format, must cover both states)
   - **清仓 / 加仓 / 不变 / 对冲 / Add / Hold**
   - If empty / watching: **买入 / 观望** (or Buy / Wait).
   - Give concise reasoning tied to the data.

   **以上仅基于公开数据的个人分析，不构成投资建议。加密货币波动极大，请自行研究并控制仓位。**

## Output Structure (flexible but complete)

Use natural language matching the conversation, but cover:

- Token basic info (name/symbol, chain, contract, main pair)
- Current price + key changes (1h / 6h / 24h) + liquidity + volume
- Security summary (honeypot? tax? open-source? major red flags + holder growth vs heat normality)
- Tags / labels / social presence if available
- Momentum / trend description
- **综合判断**: 看涨 / 看跌 / 不确定
- **持仓策略** + **空仓策略**
- Brief reasoning + risk note

## Important Rules

- Prefer live data over cached knowledge. Always fetch fresh when analyzing a specific address.
- If data is sparse (new token, no liquidity, API error), say so clearly and default to **不确定 + 观望**.
- Do not give precise entry/exit prices or leverage advice unless the user explicitly asks and data supports it.
- For Solana memecoins especially, emphasize high risk and rapid change.
- Keep responses concise unless the user requests deeper analysis.

## Reference Files

- See `references/data-sources.md` for exact endpoints, chain ID mappings, and example curl commands.
- See `references/security-checklist.md` for the most important GoPlus fields to highlight.