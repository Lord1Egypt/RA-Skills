# ClawTrade-BNB — OpenClaw Skill

**Autonomous DeFi trading agent with explainability, multi-agent UI, and one-click activation.**

> Install it. Configure it. Activate it. Watch it trade.

---

## What It Does

**ClawTrade-BNB** is a production-ready, autonomous yield farming and rebalancing agent for BNB Chain. It:

- ✅ Executes 3 intelligent trading strategies every 60 seconds
- ✅ Generates real on-chain transactions (verified on BscScan)
- ✅ Shows WHY every decision was made (explainability panel)
- ✅ Monitors agent team in real-time (multi-agent UI)
- ✅ Learns and improves automatically (reinforced learning)
- ✅ Supports 3 risk profiles (conservative/balanced/aggressive)
- ✅ Can run in suggest-only mode (no TX, just proposals)

---

## Quick Start (3 Steps)

### 1. Install & Setup
```bash
# Install dependencies
npm install

# Copy config
cp .env.example .env

# Edit .env with your testnet private key
nano .env
# (Add PRIVATE_KEY=your_key)
```

### 2. Start Agent + Dashboard
```bash
npm run start
```

Output:
```
✅ Agent API: http://localhost:3001
✅ Dashboard: http://localhost:5173
✅ Network: testnet
```

### 3. Open Browser
```
http://localhost:5173
```

Then:
1. Click "Activate Agent"
2. Choose risk profile (conservative/balanced/aggressive)
3. Watch live activity feed
4. Click "WHY" on actions to see decisions
5. Click TX hash → BscScan proof

---

## Configuration (.env)

```bash
# ⚠️ SECURITY: Use testnet keys only. Never commit real keys.

PRIVATE_KEY=6d816d...          # Your wallet private key (testnet)
RPC_URL=https://bsc-testnet... # BNB Testnet RPC (default provided)
NETWORK=testnet                # testnet or mainnet
OPERATOR_MODE=auto_execute     # auto_execute or suggest_only
RISK_PROFILE=balanced          # conservative, balanced, aggressive
AGENT_PORT=3001                # Agent API port
UI_PORT=5173                   # Dashboard port
DEMO_MODE=true                 # Use env wallet (no wallet connect needed)
```

### Risk Profiles

| Profile | Threshold | APR Delta | Gas Limit | Concentrate | Use Case |
|---------|-----------|-----------|-----------|-------------|----------|
| **Conservative** 🛡️ | $30 | 3.0% | 1.5x | No | Safe, steady |
| **Balanced** ⚖️ | $25 | 2.0% | 2.0x | Yes (mild) | Recommended |
| **Aggressive** 🚀 | $15 | 1.0% | 1.2x | Yes (strong) | High-yield |

---

## Commands

```bash
# Start everything
npm run start

# Start only agent (no UI)
npm run agent start

# Start only dashboard
npm run dev:dashboard

# Show status
npm run status

# Tail logs
npm run logs [--limit 20] [--filter HARVEST]

# Switch network
npm run network testnet|mainnet

# Show metrics
npm run metrics [--json]

# Show demo checklist
npm run demo

# CLI help
npm run help
```

---

## Dashboard UI

### Landing Page (/)
- Product overview (15 seconds)
- Key features
- Quick links to app

### Operator Panel (/app)

**Left Sidebar:**
- Operator (connect wallet, select profile, activate)
- Live Activity (last 20 actions)
- Analytics (metrics, performance)
- Settings (network, mode, risk profile)

**Main Content:**
- Agent Team card (strategy/risk/execution/learning/narrator)
- Live activity feed with explainability
- Status indicator (🟢 active, 🔴 error)

### Explainability Drawer

Click "WHY" on any action to see:
```json
{
  "decision": {
    "profile": "balanced",
    "mode": "auto_execute",
    "confidence": 0.95,
    "rules_triggered": [
      "pending_yield_above_threshold",
      "acceptable_gas_ratio"
    ],
    "metrics_snapshot": {
      "yield_usd": 50.00,
      "gas_usd": 5.50,
      "aprs": { "vault1": 8.5, "vault2": 6.2 },
      "delta_pct": 2.3
    },
    "agent_trace": [
      { "agent": "CompoundYield", "message": "Pending yield $50 exceeds threshold", "ts": "18:00:00" },
      { "agent": "GasOptimizer", "message": "Gas cost acceptable (2.1x threshold)", "ts": "18:00:02" }
    ]
  }
}
```

---

## API Endpoints

The skill exposes an HTTP API for UI and integrations:

```bash
# Health check
curl http://localhost:3001/api/health

# Current status
curl http://localhost:3001/api/status

# Performance metrics
curl http://localhost:3001/api/metrics

# Recent actions (limit=20)
curl http://localhost:3001/api/actions?limit=20

# Action detail with explainability
curl http://localhost:3001/api/actions/cycle-42

# Activate operator
curl -X POST http://localhost:3001/api/operator/activate \
  -H "Content-Type: application/json" \
  -d '{"profile":"balanced"}'

# Pause agent (safe)
curl -X POST http://localhost:3001/api/operator/pause

# Switch mode
curl -X POST http://localhost:3001/api/operator/mode \
  -H "Content-Type: application/json" \
  -d '{"mode":"suggest_only"}'
```

---

## Demo Flow (60 Seconds)

**0:00** — Open http://localhost:5173 (dashboard landing)

**0:10** — Click "Open App"

**0:15** — UI loads (Operator + Agent Team visible)

**0:20** — Select risk profile → "Balanced"

**0:25** — Click "Activate Agent"

**0:30** — First cycle executes, action appears in feed

**0:40** — Click "WHY" on the action → explainability panel opens

**0:45** — Click TX hash → BscScan opens (proof of execution)

**0:55** — Show agent team monitoring live activity

**1:00** — "This agent is autonomous. It executes every 60 seconds."

---

## Architecture

```
Skill Root
├── skill.json           (OpenClaw manifest)
├── package.json         (dependencies + scripts)
├── .env.example         (configuration template)
├── README_SKILL.md      (this file)
│
├── src/
│  ├── cli.js           (command interface)
│  ├── risk-profiles.js (strategy parameters)
│  ├── defi-strategy-engine.js (core execution)
│  ├── reinforced-learning.js (auto-optimization)
│  ├── performance-analytics.js (metrics)
│  └── network-switcher.js (testnet ↔ mainnet)
│
├── server.js           (API + log reader)
├── api/                (REST endpoints)
│  └── logs.js
│
├── dashboard/          (React frontend)
│  └── src/
│     ├── App.tsx       (main UI)
│     └── components/
│        ├── Operator.tsx
│        ├── AgentTeam.tsx
│        ├── ActivityFeed.tsx
│        └── Explainability.tsx
│
├── execution-log.jsonl (append-only action log)
└── performance-metrics.json (cumulative metrics)
```

---

## Troubleshooting

### "RPC connection failed"
- Check RPC_URL in .env
- Fallback: https://bsc-testnet.publicnode.com

### "Private key invalid"
- Ensure PRIVATE_KEY is hex (0x...) or raw
- Use testnet wallet only (no mainnet keys in demo)

### Port already in use
- Change AGENT_PORT or UI_PORT in .env
- Or kill existing process: `lsof -ti:3001 | xargs kill -9`

### No logs appearing
- Wait for first cycle (60 seconds)
- Check wallet balance (needs > 0.01 BNB testnet)
- Run `npm run logs` to see what's there

### Dashboard blank / API 404
- Ensure server started: `npm run start`
- Check console for errors
- Try localhost:3001/api/health

---

## Security Notes

⚠️ **DO NOT:**
- Commit .env or real private keys to git
- Use mainnet keys in demo mode
- Share PRIVATE_KEY in logs or screenshots

✅ **DO:**
- Use testnet wallet for development
- Use hardware wallet for mainnet
- Enable suggest_only mode if unsure

---

## Hackathon Features

This skill delivers the 3 hackathon-winning features:

### 1️⃣ One-Click Yield Operator
- User activates via UI button
- Agent executes 3 strategies autonomously
- No manual TX needed

### 2️⃣ Explainability Panel
- Click "WHY" on any action
- See decision rules + confidence
- Full agent trace (who did what, when)
- Metrics snapshot at decision time

### 3️⃣ Multi-Agent Visual UI
- Real-time team monitoring
- Strategy / Risk / Execution / Learning / Narrator cards
- Live activity feed with agent attribution
- Status pills + color-coded outcomes

---

## Further Reading

- [SKILL.md](./SKILL.md) — Full skill manifest
- [REPLICATION_GUIDE.md](./REPLICATION_GUIDE.md) — Step-by-step setup for others
- [GitHub](https://github.com/open-web-academy/clawtrade-bnb) — Source code

---

## Support

**Issue?**
1. Check troubleshooting above
2. Run `npm run logs` to see recent actions
3. Check RPC + wallet balance
4. Open GitHub issue with `npm run logs` output

**Want to contribute?**
- Fork the repo
- Create feature branch
- Submit PR with tests

---

**Version:** 1.1.0  
**License:** MIT  
**Status:** Production-ready for hackathon + beyond  
