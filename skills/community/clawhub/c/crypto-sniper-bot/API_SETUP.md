# API Configuration Guide

This guide explains how to obtain and configure the required API keys for the Crypto Sniper Bot.

## Required APIs

### 1. Bitquery API (Recommended)

Bitquery provides real-time blockchain data for both pump.fun (Solana) and four.meme (BSC).

**How to get:**
1. Visit https://bitquery.io/
2. Sign up for a free account
3. Go to Dashboard → API Keys
4. Copy your API key
5. Add to `.env`: `BITQUERY_API_KEY=your_key_here`

**Free Tier:**
- 10,000 queries per month
- Real-time streaming data
- GraphQL API access

**Pricing:**
- Free: $0/month (10K queries)
- Developer: $49/month (100K queries)
- Professional: $299/month (1M queries)

### 2. Solana RPC Endpoint (Optional but Recommended)

For better performance and reliability, use a dedicated RPC provider.

**Options:**

#### QuickNode (Recommended)
1. Visit https://www.quicknode.com/
2. Sign up and create a Solana endpoint
3. Copy the HTTPS endpoint
4. Add to `.env`: `SOLANA_RPC_URL=your_endpoint_here`

**Free Tier:**
- 50M requests per month
- 99.9% uptime
- Global edge network

#### Helius
1. Visit https://www.helius.dev/
2. Create a free account
3. Get your RPC endpoint
4. Add to `.env`

**Free Tier:**
- 100K requests per day
- Enhanced APIs
- Priority support

#### Alchemy
1. Visit https://www.alchemy.com/
2. Create Solana app
3. Copy endpoint
4. Add to `.env`

**Free Tier:**
- 300M compute units per month
- Dashboard analytics
- Webhooks

### 3. BSC RPC Endpoint (Optional)

For four.meme monitoring on Binance Smart Chain.

**Public Endpoints (Free):**
```
https://bsc-dataseed.binance.org
https://bsc-dataseed1.defibit.io
https://bsc-dataseed1.ninicoin.io
```

**Private Providers:**
- QuickNode: https://www.quicknode.com/
- Ankr: https://www.ankr.com/
- GetBlock: https://getblock.io/

## Configuration

### Complete .env Example

```env
# Wallet Configuration
WALLET_PRIVATE_KEY=your_solana_wallet_private_key_base58

# Trading Strategy
BUY_AMOUNT=0.1
TAKE_PROFIT_PERCENT=50
STOP_LOSS_PERCENT=30
MAX_POSITIONS=10
MIN_LIQUIDITY=1000

# API Keys
BITQUERY_API_KEY=BQYxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# RPC Endpoints
SOLANA_RPC_URL=https://your-quicknode-endpoint.solana-mainnet.quiknode.pro/xxxxx/
BSC_RPC_URL=https://bsc-dataseed.binance.org

# Notification Channels
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxxxx/xxxxx
EMAIL_HOST=smtp.gmail.com
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
EMAIL_TO=recipient@email.com

# SkillPay
SKILLPAY_API_KEY=sk_e390b52cb259fc4f4aa1489547a48375d72876acdee75de57101d9e0e833fcb7

# Server
PORT=3001
```

## Testing Your Configuration

### Test API Connectivity

```bash
npm run test-api
```

This will test:
- ✅ Bitquery API connection
- ✅ Jupiter Aggregator access
- ✅ Wallet initialization
- ✅ RPC endpoint connectivity

### Expected Output

```
🧪 Testing API Integration

1. Testing PumpFun Monitor...
✅ PumpFun Monitor initialized
   Found X tokens from pump.fun

2. Testing FourMeme Monitor...
✅ FourMeme Monitor initialized
   Found X tokens from four.meme

3. Testing Jupiter Aggregator Integration...
✅ Jupiter quote successful
   Input amount: 1 SOL
   Output amount: XXX USDC

4. Testing Wallet System...
✅ Wallet initialized successfully
   SOL Balance: X.XXXX SOL
```

## Troubleshooting

### "Bitquery API key not configured"
- Add `BITQUERY_API_KEY` to your `.env` file
- Verify the key is correct
- Check your Bitquery account status

### "Jupiter quote failed"
- Check internet connectivity
- Verify Solana RPC endpoint is working
- Try using a different RPC provider
- Check if Jupiter API is experiencing downtime

### "Wallet initialization failed"
- Verify private key is in base58 format
- Check that the key is valid
- Ensure sufficient SOL balance for transactions

### "Rate limit exceeded"
- Upgrade your Bitquery plan
- Use a private RPC endpoint
- Reduce monitoring frequency

## Cost Estimation

### Free Tier (Recommended for Testing)
- Bitquery: Free (10K queries/month)
- QuickNode: Free (50M requests/month)
- Total: $0/month

### Production Setup
- Bitquery Developer: $49/month
- QuickNode Discover: $49/month
- Total: ~$98/month

### High-Volume Trading
- Bitquery Professional: $299/month
- QuickNode Build: $299/month
- Total: ~$598/month

## Security Best Practices

1. **Never commit `.env` file**
   - Add to `.gitignore`
   - Use environment variables in production

2. **Rotate API keys regularly**
   - Change keys every 90 days
   - Use different keys for dev/prod

3. **Monitor API usage**
   - Set up alerts for rate limits
   - Track costs in provider dashboards

4. **Use dedicated wallets**
   - Separate wallet for bot trading
   - Keep only necessary funds

## Support

For API-related issues:
- Bitquery: https://discord.gg/bitquery
- QuickNode: https://discord.gg/quicknode
- Jupiter: https://discord.gg/jup

For bot issues:
- Check logs in console
- Review CHANGELOG.md
- Test with `npm run test-api`
