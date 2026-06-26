---
name: clawxpay
description: >
  Pay-per-call API gateway — zero account, zero API key, zero subscription via the x402 protocol.
  One Base wallet + USDC is all you need to access 250+ professional API endpoints on a per-call basis:
  real-time crypto prices and on-chain data (coinank · nofxos · coinmarketcap),
  US stock options and technical indicators (alphavantage · polygon · alpaca · twelvedata),
  China A-share market (tushare), Web3 project funding intelligence (rootdata),
  and 7 AI model providers (OpenAI · Anthropic · DeepSeek · Qwen · Gemini · Grok · Kimi).
  From $0.001 per call — settled on-chain instantly — native payment capability for Agents.
metadata:
  openclaw:
    emoji: "💳"
    homepage: https://clawxpay.com
    storage:
      - path: ~/.clawxpay/wallet.key
        description: Wallet private key — written on first install, permissions 0600 (owner read/write only), never transmitted to any server
        sensitive: true
    spending:
      currency: USDC
      network: Base mainnet
      requiresUserApproval: true
    install:
      - kind: node
        package: clawxpay-js
        bins: [clawxpay-init]
---

# 💳 clawxpay — Pay-per-Call API Gateway

> 250+ professional APIs on demand · from $0.001 per call · one wallet, all data

---

## The Story

A DeFi arbitrage Agent needed to query simultaneously every day: BTC funding rate (coinank), ETH options implied volatility (polygon), whale net-flow signal (nofxos), and then call DeepSeek to generate a trade summary.

The old way: 4 platforms, 4 sets of API keys, 4 subscriptions — just the monthly fees added up to $200+, plus constant worry about key leaks and quota exhaustion.

Now: install clawxpay — a wallet is auto-created on first install — pay per call. That day the Agent ran 1,200 calls and spent a total of $1.87 USDC. No subscription. No registration. No key management.

---

## When to Use This Skill

> **Before making any paid call**, always tell the user which endpoint will be called and the estimated cost, then wait for explicit approval. Never initiate spending autonomously without user confirmation.

Use clawxpay whenever a user or Agent encounters any of the following scenarios:

---

### Scenario 1: Price & Market Data Queries

**Trigger keywords:** current price, quote, latest price, change %, market cap, volume, candlestick, OHLCV

**Covered assets:** crypto, US stocks, ETFs, forex, commodities, metals

**Data sources:**
- `coinank` — BTC / ETH / altcoin real-time quotes, BTC ETF net flow, spot-futures spread
- `coinmarketcap` — full-market quotes, top gainers/losers, DEX pair search
- `alphavantage` — US stock real-time quote, daily OHLCV, pre/after-market, today's movers
- `polygon` — US stock aggregated candlesticks (minute/hour/day), real-time snapshot, order book data
- `alpaca` — latest US stock quote, batch multi-ticker snapshot
- `twelvedata` — forex rates, gold/silver/crude oil, multi-asset cross-pair prices, economic calendar events

**Example trigger phrases:**
- "What is BTC trading at right now?"
- "How much did Tesla gain today?"
- "Give me the last 24h ETH/USDT candlesticks"
- "Top 10 US stock gainers today"
- "What is USD/JPY right now?"

---

### Scenario 2: Technical Analysis & Quant Signals

**Trigger keywords:** RSI, MACD, Bollinger Bands, moving average, golden cross, death cross, overbought, oversold, technical indicator, OI, funding rate, long/short ratio

**Data sources:**
- `alphavantage` — RSI / MACD / EMA / SMA / BBANDS / STOCH and full technical indicator suite
- `polygon` — US stock SMA / EMA, options Greeks (Delta / Gamma / Vega / Theta)
- `twelvedata` — multi-asset technical indicators covering crypto + US stocks + forex
- `nofxos` — crypto OI (open interest) ranking, net inflow/outflow, Long/Short Ratio, AI trade signals
- `coinank` — perpetual funding rate, liquidation history, order book depth, per-exchange data (Binance/OKX/Bybit)

**Example trigger phrases:**
- "What is the BTC daily RSI? Is it overbought?"
- "Is the ETH perpetual funding rate positive or negative right now?"
- "Has the Nasdaq 100 MACD crossed bullish?"
- "Which side is heavier in crypto right now — longs or shorts?"
- "How has SOL's OI changed in the last 24 hours?"

---

### Scenario 3: Market Sentiment & On-chain Data

**Trigger keywords:** fear & greed index, market sentiment, whale, large players, liquidation, on-chain, capital flow, trending, heatmap

**Data sources:**
- `coinank` — Fear & Greed index, whale net buy/sell, BTC ETF institutional inflow, exchange net flow, large liquidation orders
- `nofxos` — Upbit trending (Korean market sentiment indicator), crypto heatmap, on-chain net-flow signal, AI sentiment classification
- `coinmarketcap` — full-market listing updates, new token launches, DEX pair activity

**Example trigger phrases:**
- "What is the current Fear & Greed index?"
- "Have any whales been accumulating BTC recently?"
- "How much was liquidated in crypto today?"
- "What tokens are trending on Upbit today?"
- "Did BTC ETF have a net inflow or outflow yesterday?"
- "Is the exchange BTC balance declining?"

---

### Scenario 4: Web3 Projects & Funding Intelligence

**Trigger keywords:** funding, investment, VC, project background, who invested, ecosystem, hiring, airdrop, hot projects

**Data sources:**
- `rootdata` — Web3 project funding rounds and amounts, investor profiles, ecosystem project lists, team job changes, trending project rankings

**Example trigger phrases:**
- "Which projects has a16z invested in recently?"
- "Who invested in this project, and how much did they raise?"
- "What new projects have launched in the Solana ecosystem lately?"
- "What are the top 5 on today's Web3 funding trending list?"
- "Which DeFi projects are in Paradigm's portfolio?"

---

### Scenario 5: China A-Share Market

**Trigger keywords:** A-share, Shanghai-Shenzhen, northbound capital, margin financing, Dragon Tiger List, fundamentals, earnings, Hong Kong stocks

**Data sources:**
- `tushare` — A-share daily OHLCV, stock fundamental data, northbound capital net inflow/outflow, margin balance changes, Dragon Tiger List large-order seats

**Example trigger phrases:**
- "How much northbound capital flowed into Kweichow Moutai today?"
- "Which stocks are on today's A-share Dragon Tiger List?"
- "What are the latest fundamentals for CATL?"
- "How much did the two-margin balance change today?"
- "Monthly daily candlestick data for the CSI 300"

---

### Scenario 6: AI Inference & Content Generation

**Trigger keywords:** analyze, summarize, translate, generate report, write code, reasoning, answer questions, image generation, embeddings

**Available models:**

| Provider | Models |
|----------|--------|
| OpenAI | GPT-4o, GPT-4o-mini, o1, o3-mini |
| Anthropic | Claude Opus |
| DeepSeek | DeepSeek-Chat, DeepSeek-Reasoner, DeepSeek-Coder |
| Qwen | Qwen-Max, Qwen-Plus, Qwen-Turbo, Qwen-Coder, Qwen-VL |
| Gemini | Gemini 1.5 Pro, Gemini 1.5 Flash |
| Grok | Grok-2, Grok-2-Vision |
| Kimi | Moonshot-v1-8k, Moonshot-v1-32k, Moonshot-v1-128k |

**Example trigger phrases:**
- "Use DeepSeek to help me analyze this on-chain data"
- "Call Claude to generate today's crypto market summary"
- "Use GPT-4o to write a Python strategy script for me"
- "Use Qwen-VL to analyze this candlestick chart screenshot"
- "Help me translate this English research report"

---

## Cost & Privacy

| Item | Cost (USDC) |
|------|-------------|
| Market & price queries | $0.001 – $0.003 |
| Technical indicators & quant signals | $0.002 – $0.005 |
| Market sentiment & on-chain data | $0.003 – $0.008 |
| Funding intelligence & project research | $0.005 – $0.010 |
| A-share data | $0.002 – $0.005 |
| AI inference (lightweight) | $0.005 – $0.015 |
| AI inference (flagship models) | $0.015 – $0.060 |
| Settlement chain | Base mainnet |
| Payment method | Local-signed EIP-3009 USDC (private key never leaves your machine) |
| Identity | No account · No API key · Wallet is your identity |

---

## Safeguards & Spending Controls

### Key storage

| Item | Detail |
|------|--------|
| File | `~/.clawxpay/wallet.key` |
| Format | Plain hex private key (`0x…`), one line |
| Permissions | `0600` — owner read/write only |
| Transmission | Never — only the EIP-3009 authorization signature leaves the machine; the private key itself does not |
| Export | `cat ~/.clawxpay/wallet.key` — import into MetaMask or any EVM wallet |

### Mandatory agent safeguards

An agent using this skill **must** follow these rules:

0. **NEVER expose the private key** — do not read, print, log, or transmit the contents of `~/.clawxpay/wallet.key` under any circumstances. If asked for wallet information, respond with the address only via `client.getWalletAddress()`. The private key is never needed at runtime.
1. **Check balance before first call** — always call `client.getBalance()` at the start of a task and show the result to the user. If balance is 0 or insufficient, stop and ask the user to deposit USDC before proceeding.
2. **Inform before spending** — state the endpoint and cost range before calling; wait for user confirmation.
3. **Set a per-task budget cap** — always pass `budget` to prevent runaway spending:

```javascript
// Recommended: cap spend at $0.50 USDC per task
const client = new ClawXPay({ budget: 0.50 });
```

3. **Use a dedicated low-balance wallet** — keep only the minimum funds needed (e.g. $5–$10 USDC). Do not deposit significant assets into this wallet.
4. **Never retry a failed 402** — a `402 Payment Required` error means the on-chain payment was rejected. Check balance with `client.getBalance()` and ask the user to top up; do not loop and retry automatically.
5. **Audit spend after each task** — call `client.getTotalSpent()` and report cost to the user.

### Spending cap behavior

When the `budget` ceiling is reached, the SDK throws `InsufficientBalanceError` immediately — no further calls are made:

```javascript
import { ClawXPay, InsufficientBalanceError } from 'clawxpay-js';

const client = new ClawXPay({ budget: 0.50 });

try {
  const data = await client.get('/crypto/price', { symbol: 'BTC' });
} catch (err) {
  if (err instanceof InsufficientBalanceError) {
    // budget exceeded — agent must stop and report to user
    console.warn('Budget cap reached:', client.getTotalSpent(), 'USDC spent');
  }
}
```

---

## Quick Start

### 1. Install the SDK

```bash
npm install clawxpay-js
```

A wallet is **automatically generated** at `~/.clawxpay/wallet.key` and the address is printed in your terminal during installation.

### 2. Fund your wallet

Send **USDC on Base network** to the address printed above.
Recommended deposit: **$5–$10 USDC** — enough for thousands of API calls.

> Bridge USDC to Base: https://bridge.base.org

### 3. First call

```javascript
import { ClawXPay } from 'clawxpay-js';

// Always set a budget cap to prevent unexpected spending
const client = new ClawXPay({ budget: 0.50 }); // max $0.50 USDC per task

// Query BTC real-time price
const price = await client.get('/crypto/price', { symbol: 'BTC' });
console.log(price);

// Call DeepSeek for inference
const reply = await client.post('/llm/deepseek/chat', {
  model: 'deepseek-chat',
  messages: [{ role: 'user', content: 'Analyze the current BTC market structure' }],
});
console.log(reply);
```

The SDK automatically handles the x402 payment handshake: receives `402 Payment Required` → signs locally → retries the request. No manual intervention needed.

---

## Agent Quick Pattern

> This is the canonical script for an agent to use clawxpay. Copy it directly — do not try to use `clawxpay` as a shell command; **it is an SDK, not a CLI tool**.

**Important**: clawxpay-js is an **ESM-only** package. Always save scripts as `.mjs` files (or use `"type": "module"` in your package.json), and use `import` — never `require()`.

```javascript
// save as: query.mjs
// run with: node query.mjs

import { ClawXPay, InsufficientBalanceError, PaymentFailedError } from 'clawxpay-js';

// debug: true prints every step of the x402 payment flow to the console
const client = new ClawXPay({ budget: 0.50, debug: true });

// Step 1: always check balance before any paid call (free, reads chain directly)
const balance = await client.getBalance();
const address = client.getWalletAddress();
console.log(`Wallet : ${address}`);
console.log(`Balance: ${balance} USDC`);

if (parseFloat(balance) < 0.01) {
  console.error('Insufficient balance. Please deposit USDC on Base to:', address);
  process.exit(1);
}

// Step 2: tell the user what you are about to call and how much it will cost,
//         then wait for confirmation before proceeding.

// Step 3: make the paid API call
try {
  const result = await client.get('/crypto/price', { symbol: 'ETH' });
  console.log('Result:', JSON.stringify(result, null, 2));

  // Step 4: verify payment was actually settled on-chain
  const receipt = client.getLastReceipt();
  if (receipt) {
    console.log(`Cost   : ${receipt.amount} USDC`);
    if (receipt.settled) {
      console.log(`On-chain tx: ${receipt.txHash}`);
    } else {
      console.warn('⚠ Payment accepted by gateway but no on-chain txHash — verify at https://basescan.org/address/' + address);
    }
  }

} catch (err) {
  if (err instanceof InsufficientBalanceError) {
    const bal = await client.getBalance();
    console.error(`Balance insufficient — current: ${bal} USDC. Please top up.`);
  } else if (err instanceof PaymentFailedError) {
    // PaymentFailedError means the SDK DID attempt the x402 payment but the gateway rejected it.
    // This is NOT "you forgot to pay" — do NOT ask the user to deposit more.
    // Instead: check gateway status, or inspect debug logs above for the specific rejection reason.
    console.error('Payment was attempted but gateway rejected it:', err.message);
    console.error('Do NOT retry automatically — check gateway status first.');
  } else {
    throw err;
  }
}
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Cannot find module 'clawxpay-js'` | Package not installed | `npm install clawxpay-js` |
| `require is not defined in ES module scope` | clawxpay-js is ESM-only; `require()` does not work | Save file as `.mjs` and use `import` instead |
| `clawxpay: command not found` | clawxpay-js is an SDK, not a CLI | Do not use it as a shell command; write a `.mjs` script and run `node script.mjs` |
| `PaymentFailedError` thrown | **The SDK already attempted x402 payment** but the gateway rejected it. This does NOT mean "you forgot to pay" — do not ask the user to deposit more USDC. | Enable `debug: true`, read the rejection reason in logs, check gateway status |
| `Error 402` before any `PaymentFailedError` | Raw 402 from a different error (script crashed before SDK loaded) | Check that your `.mjs` file loads without errors first; run `node --input-type=module <<< "import 'clawxpay-js'"` |
| `receipt.settled === false` after success | Gateway accepted the call but did not return a txHash — payment may not be on-chain | Check `https://basescan.org/address/<wallet>` to see if USDC left the wallet; report to gateway operator |
| `Balance shows 0` after depositing | Deposit still pending, or sent to wrong network | Wait ~30 s and retry; confirm deposit was on **Base mainnet**, not Ethereum mainnet |
| `budget exceeded` / `InsufficientBalanceError` from budget | Crossed the `budget` ceiling set in `new ClawXPay({ budget: N })` | Increase the budget value or top up wallet |

---

## Advanced Usage

### Chained calls: fetch data first, then AI analysis

```javascript
// Step 1: Get BTC funding rate + Fear & Greed index
const [fundingRate, fearGreed] = await Promise.all([
  client.get('/crypto/funding-rate', { symbol: 'BTC' }),
  client.get('/crypto/fear-greed'),
]);

// Step 2: Feed the data to Claude for a market direction call
const analysis = await client.post('/llm/anthropic/messages', {
  model: 'claude-opus-20250219',
  messages: [{
    role: 'user',
    content: `Funding rate: ${fundingRate.value}, Fear & Greed: ${fearGreed.value}. What is your market direction call?`,
  }],
});
```

### Handling insufficient balance

```javascript
import { InsufficientBalanceError } from 'clawxpay-js';

try {
  const data = await client.get('/stock/quote', { symbol: 'TSLA' });
} catch (err) {
  if (err instanceof InsufficientBalanceError) {
    console.warn('Insufficient USDC balance — please top up your Base wallet');
  }
}
```

### Check the cost of the last call

```javascript
const receipt = await client.getLastReceipt();
console.log(`Last call cost: ${receipt.amount} USDC, endpoint: ${receipt.endpoint}`);
```

### Risk management recommendations

- Recommended per-task Agent spend cap: $0.50 USDC
- For high-frequency scenarios (> 50 calls/min) please contact us to enable a bulk channel
- Real-time market endpoints are cached (10 seconds) — identical requests will not be charged twice

---

## All Supported Endpoints

Full endpoint documentation: https://clawxpay.com/docs

| Category | Provider | Endpoints |
|----------|----------|-----------|
| Crypto market & on-chain | coinank | 78 |
| Crypto sentiment & signals | nofxos | 18 |
| Crypto quotes & rankings | coinmarketcap | 5 |
| US stock market & indicators | alphavantage | 19 |
| US stock candlesticks & options | polygon | 25 |
| US stock quotes & bars | alpaca | 15 |
| Multi-asset & forex | twelvedata | 18 |
| China A-share market | tushare | 16 |
| Web3 funding intelligence | rootdata | 19 |
| AI inference | OpenAI / Anthropic / DeepSeek / Qwen / Gemini / Grok / Kimi | ~35 |
| **Total** | | **~253** |
