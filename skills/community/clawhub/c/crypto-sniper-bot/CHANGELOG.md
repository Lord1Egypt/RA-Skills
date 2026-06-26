# Changelog

## [1.1.0] - 2026-03-06

### Added - Real API Integration
- ✅ **Bitquery GraphQL API** integration for pump.fun monitoring
  - Real-time token launch detection
  - Token price and liquidity data
  - Holder count and market cap tracking

- ✅ **Jupiter Aggregator V6** integration for Solana trading
  - Best price routing across all Solana DEXs
  - Automatic slippage protection
  - Dynamic compute unit limits
  - Priority fee optimization

- ✅ **Four.meme Bitquery API** integration
  - BSC token monitoring support
  - Real-time trade data
  - Bonding curve tracking

- ✅ **Multi-chain support**
  - Solana (pump.fun)
  - BSC (four.meme)
  - Chain-specific trading logic

### Improved
- Enhanced token monitoring with GraphQL queries
- Better error handling for API failures
- Fallback mechanisms for API downtime
- More accurate price fetching
- Real token balance checking

### Configuration
- Added `BITQUERY_API_KEY` for token monitoring
- Added `SOLANA_RPC_URL` for custom RPC endpoints
- Added `BSC_RPC_URL` for BSC network access

### Technical Details
- **PumpFun Monitor**: Uses Bitquery GraphQL with PumpPortal fallback
- **FourMeme Monitor**: Uses Bitquery GraphQL for BSC
- **Trading Engine**: Jupiter V6 API for optimal swap execution
- **Price Feeds**: Real-time from Jupiter quotes

### API Endpoints Used
1. **Bitquery Streaming API**: `https://streaming.bitquery.io/graphql`
2. **Jupiter Quote API**: `https://quote-api.jup.ag/v6`
3. **PumpPortal API**: `https://pumpportal.fun/api` (fallback)

### Requirements
- Bitquery API key (free tier available)
- Solana RPC endpoint (public or private)
- BSC RPC endpoint (optional, for four.meme)

### Migration from 1.0.0
1. Update `.env` with new API keys:
   ```env
   BITQUERY_API_KEY=your_key_here
   SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
   BSC_RPC_URL=https://bsc-dataseed.binance.org
   ```

2. No code changes required - fully backward compatible

### Known Limitations
- BSC trading not yet implemented (monitoring only)
- Requires Bitquery API key for full functionality
- Public RPC endpoints may have rate limits

---

## [1.0.0] - 2026-03-06

### Initial Release
- Basic token monitoring (placeholder APIs)
- Trading engine framework
- Position management
- Take-profit/stop-loss strategies
- Multi-channel notifications
- SkillPay integration
