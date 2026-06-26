# Pocket Options Trading Bot

AI-powered binary options trading bot for Pocket Options with recursive learning and Martingale recovery strategy.

## ⚠️ Risk Warning

**Binary options trading is extremely high-risk. This bot is experimental software.**

- Only trade with money you can afford to lose completely
- Start with paper trading / demo account
- Never exceed your risk limits
- Past performance does not guarantee future results

## Features

### 🤖 AI Learning System
- **Weighted Indicators**: RSI, MACD, Bollinger Bands, Volume, Price Action
- **Recursive Learning**: Automatically adjusts indicator weights based on win/loss
- **Pattern Recognition**: Identifies successful trading patterns from history
- **Adaptive Confidence**: Reduces trading during losing streaks

### 💰 Martingale Strategy
- **Progressive Recovery**: 1 → 2 → 4 → 8 simultaneous trades
- **Smart Sizing**: Each tier doubles position count, not individual size
- **Safety Cap**: Maximum 8 trades (configurable)
- **Auto Reset**: Returns to single trade after any win

### 🛡️ Risk Management
- **Circuit Breaker**: Automatic halt at 20% daily loss
- **Loss Streak Protection**: Stops after 3 consecutive losses
- **Position Limits**: Maximum risk per Martingale tier
- **Price Manipulation Detection**: Avoids honeypot situations

### 🕵️ Stealth & Anti-Detection
- **Browser Fingerprint Masking**: Randomized user agents, viewports, timezones
- **WebDriver Concealment**: Removes automation detection flags
- **Human-Like Behavior**: Variable timing, hesitation, typing speed
- **Unpredictable Patterns**: Randomized amounts, thresholds, intervals
- **Break Periods**: Simulates human fatigue with random pauses

### 📊 Performance Tracking
- **P&L Statistics**: Daily, weekly, monthly, all-time
- **Win Rate Analysis**: Track success percentage
- **Trade Journal**: Complete history with timestamps
- **Best/Worst Trades**: Performance extremes

## Architecture

```
src/
├── core/
│   ├── martingale.ts           # Martingale strategy manager
│   ├── pnl-tracker.ts          # Profit/loss tracking
│   ├── risk-manager.ts         # Circuit breaker & limits
│   ├── manipulation-detector.ts # Price manipulation detection
│   └── trading-decision.ts     # Decision engine with randomization
├── indicators/
│   ├── base-indicator.ts       # Base class for all indicators
│   ├── rsi.ts                  # RSI indicator
│   ├── macd.ts                 # MACD indicator (TODO)
│   └── bollinger.ts            # Bollinger Bands (TODO)
├── browser/
│   ├── stealth.ts              # Browser fingerprint masking
│   └── pocket-options-client.ts # Browser automation with stealth
├── utils/
│   ├── logger.ts               # Winston logger
│   └── humanization.ts         # Human behavior simulation
├── learning/
│   └── learning-engine.ts      # AI learning system (TODO)
└── index.ts                     # Main entry point (TODO)
```

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Install agent-browser (for browser automation)

```bash
npm install -g agent-browser
agent-browser install
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Login to Pocket Options (One-time)

```bash
# Open browser, login manually, save session
agent-browser open https://pocketoption.com
# ... complete login ...
agent-browser state save ./data/browser-session/pocket-auth.json
```

## Usage

### Development Mode

```bash
npm run dev
```

### Production Build

```bash
npm run build
npm start
```

### Paper Trading

Set `BASE_TRADE_AMOUNT=0` in `.env` to simulate trades without real money.

## Configuration

Key settings in `.env`:

```bash
# Trading
BASE_TRADE_AMOUNT=10           # Base amount per trade ($)
MAX_DAILY_LOSS_PERCENT=20      # Circuit breaker threshold
MARTINGALE_MAX_TIER=3          # Max tier (0=1, 1=2, 2=4, 3=8)

# AI Learning
LEARNING_RATE=0.1              # How fast weights adjust
MIN_CONFIDENCE_THRESHOLD=0.6   # Minimum confidence to trade

# Safety
STOP_ON_LOSS_STREAK=3          # Halt after N consecutive losses
CIRCUIT_BREAKER_ENABLED=true   # Enable auto-halt on limits
```

## How It Works

### 1. Market Analysis
- Fetches 1-minute candle data from Pocket Options
- Runs all technical indicators (RSI, MACD, Bollinger, etc.)
- Each indicator provides: BUY / SELL / NEUTRAL signal

### 2. Weighted Decision
```typescript
totalScore = Σ(indicator.signal × indicator.weight)
confidence = totalScore / totalWeights

if (confidence > threshold && !manipulation detected):
  → Execute trade
```

### 3. Trade Execution
- Checks risk manager (circuit breaker, loss streak)
- Determines Martingale tier (1, 2, 4, or 8 trades)
- Executes trades simultaneously via browser automation
- Sets 5-minute expiration on all trades

### 4. Result Processing
- Waits for expiration
- Records win/loss for each trade
- Updates P&L tracker
- Adjusts indicator weights (winners up, losers down)
- Updates Martingale tier

### 5. Learning Loop
- Identifies similar past patterns
- Calculates success rate for this pattern
- Adjusts strategy confidence
- Increases manipulation sensitivity if losing streak

## Indicator Weights

Indicators start with default weights and self-adjust:

| Indicator | Initial Weight | Adjusts Based On |
|-----------|----------------|------------------|
| RSI       | 0.8            | Overbought/oversold accuracy |
| MACD      | 0.7            | Trend change accuracy |
| Bollinger | 0.6            | Volatility breakout accuracy |
| Volume    | 0.5            | Volume spike accuracy |
| Price Action | 0.6         | Pattern recognition accuracy |

**Learning Rate**: After each trade, winner weights increase by 0.1, losers decrease by 0.1

## Martingale Example

```
Trade 1: $10 → LOSS (-$10)
  ↓
Trade 2: 2× $10 = $20 total → LOSS (-$30 total)
  ↓
Trade 3: 4× $10 = $40 total → LOSS (-$70 total)
  ↓
Trade 4: 8× $10 = $80 total → WIN (+$10 net profit)
  ↓
Reset to Trade 1
```

## Price Manipulation Detection

Bot avoids trading when detecting:

1. **Volume Spike + No Price Movement**: Fake volume
2. **Repeated Wick Patterns**: Stop hunting
3. **Abnormally Tight Spread**: Low liquidity trap
4. **Sudden Reversal Without Volume**: Artificial move

## P&L Dashboard

```
╔══════════════════════════════════════════════════╗
║       Pocket Options Bot - P&L Summary           ║
╠══════════════════════════════════════════════════╣
║  Daily:   +$45.00     (12 trades, 67% win)       ║
║  Weekly:  +$120.00    (45 trades, 58% win)       ║
║  Monthly: +$380.00    (180 trades, 55% win)      ║
║  AllTime: +$1,240.00  (520 trades, 54% win)      ║
╚══════════════════════════════════════════════════╝
```

## Code Foundation Sources

This project is built using patterns from:

- **base-trader-1.1.1**: Risk management, position sizing, circuit breakers
- **solana-funding-arb-2.1.0**: P&L tracker, arbitrage engine architecture
- **agent-browser-clawdbot**: Browser automation via agent-browser CLI
- **browser-use-1.0.0**: Cloud browser fallback option

## Development Roadmap

### ✅ Completed
- [x] Project structure and configuration
- [x] Martingale strategy manager (1→2→4→8)
- [x] P&L tracker with statistics
- [x] Risk manager with circuit breaker
- [x] Price manipulation detector
- [x] Base indicator system with auto-learning
- [x] RSI indicator implementation
- [x] **Browser stealth system** (user agent masking, WebDriver hiding)
- [x] **Human behavior simulation** (timing, hesitation, patterns)
- [x] **Trading decision engine** with randomization
- [x] **Pocket Options client** with anti-detection

### 🚧 In Progress / TODO
- [ ] MACD indicator
- [ ] Bollinger Bands indicator
- [ ] Volume analysis indicator
- [ ] Chart data extraction from Pocket Options DOM
- [ ] Learning engine (pattern recognition)
- [ ] Main trading loop
- [ ] Indicator manager (combines all indicators)
- [ ] CLI interface
- [ ] Dashboard/monitoring
- [ ] Backtesting system
- [ ] Paper trading mode

## Testing

```bash
# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

## License

MIT

## Disclaimer

This software is provided for educational purposes only. Use at your own risk. The author is not responsible for any financial losses incurred while using this bot.

**NOT FINANCIAL ADVICE**
