# Bitget Trader 🟦

Professional Bitget integration for automated grid trading and portfolio management.

## 🚀 Quick Start

### Setup Credentials

Save to `/Users/zongzi/.openclaw/workspace/bitget_data/config.json`:
```json
{
  "apiKey": "bg_your_api_key",
  "secretKey": "your_secret_key",
  "passphrase": "your_passphrase",
  "isSimulation": false
}
```

### API Key Requirements
- **Permissions**: Spot Read + Spot Trade
- **IP Whitelist**: Recommended but optional
- **Passphrase**: Required (set when creating API key)

## 📊 Basic Commands

### Check Balance
```bash
node /Users/zongzi/.openclaw/workspace/bitget_data/check-balance.js
```

### Monitor Grid Status
```bash
node /Users/zongzi/.openclaw/workspace/bitget_data/monitor-grid.js
```

### Start Grid Trading
```bash
node /Users/zongzi/.openclaw/workspace/bitget_data/start-simple.js
```

### Cancel All Orders
```bash
node /Users/zongzi/.openclaw/workspace/bitget_data/cancel-all.js
```

## 🎯 Grid Trading System

### Configuration

Edit `/Users/zongzi/.openclaw/workspace/bitget_data/grid_settings.json`:

```json
{
  "btc": {
    "symbol": "BTCUSDT",
    "gridNum": 50,
    "priceMin": 63000,
    "priceMax": 70000,
    "amount": 20,
    "maxPosition": 400,
    "sellOrders": 10,
    "buyOrders": 10
  },
  "eth": {
    "symbol": "ETHUSDT",
    "gridNum": 30,
    "priceMin": 1800,
    "priceMax": 2700,
    "amount": 4,
    "maxPosition": 150
  }
}
```

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `symbol` | Trading pair | BTCUSDT |
| `gridNum` | Number of grid levels | 50 |
| `priceMin` | Minimum price | 63000 |
| `priceMax` | Maximum price | 70000 |
| `amount` | USDT per order | 20 |
| `maxPosition` | Max total position | 400 |
| `sellOrders` | Max sell orders | 10 |
| `buyOrders` | Max buy orders | 10 |

## 📈 Available Scripts

### Core Trading
| Script | Purpose |
|--------|---------|
| `monitor-grid.js` | Monitor all grid strategies |
| `start-simple.js` | Start all grids |
| `cancel-all.js` | Cancel all orders |
| `check-balance.js` | Check account balance |

### Analysis & Optimization
| Script | Purpose |
|--------|---------|
| `grid-optimizer.js` | Optimize grid parameters |
| `kline-analyzer.js` | Analyze K-line data |
| `trade-analyzer.js` | Analyze trade history |
| `quick-report.js` | Generate quick report |

### Dynamic Adjustment
| Script | Purpose |
|--------|---------|
| `dynamic-adjust.js` | Dynamic grid adjustment |
| `dynamic-rebalance.js` | Portfolio rebalancing |
| `apply-scheme-a.js` | Apply optimization scheme A |

### Single Coin Operations
| Script | Purpose |
|--------|---------|
| `start-eth.js` | Start ETH grid |
| `deploy-bnb-grid.js` | Deploy BNB grid |
| `buy-eth-market.js` | Buy ETH at market price |

## 🔧 Advanced Features

### 1. Multi-Coin Grid Support
Supports concurrent grid trading for multiple coins:
- BTCUSDT (Bitcoin)
- ETHUSDT (Ethereum)
- SOLUSDT (Solana)
- BNBUSDT (Binance Coin)

### 2. Dynamic Grid Adjustment
Automatically adjusts grid parameters based on:
- Market volatility
- Price trends
- Order fill rates
- Balance availability

### 3. Risk Management
- **Position Limits**: Configurable `maxPosition` per coin
- **Order Throttling**: Prevents API rate limiting
- **Balance Check**: Validates sufficient USDT before deployment

### 4. Comprehensive Logging
All operations logged to:
- `grid_monitor.log` - Grid status updates
- `monitor.log` - General monitoring logs
- `trade-analysis.log` - Trade analysis results

## 📊 Reporting

### Generate Reports

```bash
# Grid status report
node /Users/zongzi/.openclaw/workspace/bitget_data/monitor-grid.js

# Trade analysis
node /Users/zongzi/.openclaw/workspace/bitget_data/trade-analyzer.js

# Quick report
node /Users/zongzi/.openclaw/workspace/bitget_data/quick-report.js
```

### Report Files
- `GRID_STATUS_REPORT.md` - Current grid status
- `GRID_OPTIMIZATION_REPORT.md` - Optimization suggestions
- `DYNAMIC_STRATEGY_REPORT.md` - Dynamic strategy analysis

## ⚠️ Risk Warning

- **Cryptocurrency trading involves significant risk**
- **Test with small amounts first**
- **Never invest more than you can afford to lose**
- **API keys should have NO withdrawal permissions**

## 🔐 Security Best Practices

1. **API Key Permissions**: Only enable Spot Read + Spot Trade
2. **IP Whitelist**: Restrict API access to your IP
3. **No Withdrawal**: Never enable withdrawal permissions
4. **Secure Storage**: Keep config.json secure (chmod 600)

## 📝 File Structure

```
bitget_data/
├── config.json                 # API credentials
├── grid_settings.json          # Grid configurations
├── monitor-grid.js             # Main monitoring script
├── start-simple.js             # Start all grids
├── cancel-all.js               # Cancel all orders
├── check-balance.js            # Check balance
├── grid-optimizer.js           # Grid optimization
├── trade-analyzer.js           # Trade analysis
├── dynamic-adjust.js           # Dynamic adjustments
├── grid_monitor.log            # Monitoring logs
└── SKILL.md                    # This file
```

## 🆘 Troubleshooting

### Common Issues

**1. Signature Mismatch**
- Check API key format (should start with `bg_`)
- Verify secret key is correct
- Ensure system time is synchronized

**2. Proxy Connection Failed**
- Ensure proxy is running on port 7897
- Check ClashX/Shadowrocket status
- Try: `curl -x http://127.0.0.1:7897 https://api.bitget.com`

**3. Insufficient Balance**
- Check USDT balance: `node check-balance.js`
- Reduce `amount` or `gridNum` in grid_settings.json
- Consider restoring original config from backup

**4. Orders Not Filling**
- Check grid price range covers current market price
- Verify order quantity meets exchange minimum
- Review grid spacing (may be too tight/wide)

## 📚 API Reference

### Bitget API v2 Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v2/spot/account` | GET | Get account info |
| `/api/v2/spot/orders` | GET | Get open orders |
| `/api/v2/spot/place-order` | POST | Place order |
| `/api/v2/spot/cancel-order` | POST | Cancel order |
| `/api/v2/spot/market-tickers` | GET | Get market prices |

### Signature Generation

```javascript
const timestamp = new Date().toISOString().split('.')[0] + '.000Z';
const method = 'GET';
const path = '/api/v2/spot/account';
const body = '';
const signStr = timestamp + method + path + body;
const signature = crypto.createHmac('sha256', secretKey).update(signStr).digest('base64');
```

---

## 🎯 Quick Commands Reference

```bash
# Monitor all grids
node monitor-grid.js

# Start trading
node start-simple.js

# Stop trading (cancel all)
node cancel-all.js

# Check balance
node check-balance.js

# Optimize grids
node grid-optimizer.js

# Analyze trades
node trade-analyzer.js

# Generate report
node quick-report.js
```

---

**Version**: 1.0.0  
**Exchange**: Bitget  
**Type**: Spot Grid Trading  
**Last Updated**: 2026-03-10
