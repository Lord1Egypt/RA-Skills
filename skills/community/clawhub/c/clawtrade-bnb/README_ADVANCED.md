# Advanced Features - Network Switching & Reinforced Learning

This document covers the advanced capabilities Alan requested:

## 1️⃣ Network Switching (Testnet ↔ Mainnet)

### Quick Start

```bash
# Check current network
node agent-cli.js network status

# Switch to testnet (default)
node agent-cli.js network testnet

# Switch to mainnet (production)
node agent-cli.js network mainnet
```

### What Changes When You Switch?

**Testnet Config:**
```json
{
  "chainId": 97,
  "rpc": "https://bsc-testnet.publicnode.com",
  "scanner": "https://testnet.bscscan.com",
  "harvestThreshold": 25,  // Lower on testnet for testing
  "gasMultiplier": 1.2     // Less conservative
}
```

**Mainnet Config:**
```json
{
  "chainId": 56,
  "rpc": "https://bsc-dataseed1.defibit.io",
  "scanner": "https://bscscan.com",
  "harvestThreshold": 100,  // Higher on mainnet for safety
  "gasMultiplier": 1.5      // More conservative gas settings
}
```

### Network Switcher Features

- ✅ **Instant switching** - No restart needed
- ✅ **Persistent** - Saves preference to `.network.json`
- ✅ **Contract mapping** - Different addresses per network
- ✅ **Gas optimization** - Auto-adjusts gas multiplier per network
- ✅ **Token prices** - Can update token prices per network
- ✅ **Scanner links** - Automatically generates correct explorer URLs

### Code Integration

```javascript
const NetworkSwitcher = require('./network-switcher');

const switcher = new NetworkSwitcher('testnet');

// Switch networks
switcher.switchNetwork('mainnet');

// Get contract addresses
const vaultAddress = switcher.getContractAddress('vault_eth_staking_001');

// Get TX links
const txLink = switcher.getTxLink('0xabc123...');
// → https://bscscan.com/tx/0xabc123...
```

---

## 2️⃣ Performance Analytics

### Get Real-Time Performance Metrics

```bash
# Quick summary
node agent-cli.js perf summary

# Detailed report
node agent-cli.js perf report

# Per-vault breakdown
node agent-cli.js perf vaults

# Strategy effectiveness
node agent-cli.js perf strategies
```

### Performance Metrics Tracked

- **Success Rate**: % of successful actions vs total
- **Realized APR**: Actual APR based on harvested yield
- **Total Harvested**: Cumulative USD harvested
- **Total Compounded**: Amount reinvested
- **Vault Performance**: Per-vault yield breakdown
- **Strategy Effectiveness**: Which strategy works best
- **Failure Patterns**: Common error reasons

### Code Integration

```javascript
const PerformanceAnalytics = require('./performance-analytics');

const analytics = new PerformanceAnalytics();

// Get summary
const summary = analytics.getPerformanceSummary();
console.log(`Success rate: ${(summary.successRate * 100).toFixed(1)}%`);
console.log(`Realized APR: ${summary.realizedAPR.toFixed(2)}%`);

// Get vault performance
const vaults = analytics.getVaultPerformance();

// Get strategy analysis
const strategies = analytics.getStrategyAnalysis();

// Generate report (prints to console)
analytics.generateReport();
```

---

## 3️⃣ Reinforced Learning System

### What It Does

The reinforced learning system automatically **learns from past failures** and **optimizes strategy parameters** in real-time.

### How It Works

1. **Analyzes execution history** - Reads `execution-log.jsonl`
2. **Identifies failure patterns** - Finds common error types
3. **Updates strategy metrics** - Tracks success rates per strategy
4. **Generates improvements** - Adjusts thresholds dynamically
5. **Saves learned state** - Persists to `learning-state.json`

### Running Learning Cycles

```bash
# Analyze history and optimize parameters
node agent-cli.js learn now

# View learning progress
node agent-cli.js learn report

# Reset learning state (if needed)
node agent-cli.js learn reset
```

### Example Learning Improvements

The system automatically learns:

**COMPOUND_YIELD Strategy:**
- If success rate > 80% → Lower harvest threshold to capture more opportunities
- If failure rate > 20% → Increase threshold to skip low-value harvests
- Confidence level increases as success improves

**REBALANCE Strategy:**
- If failure rate > 20% → Increase APR delta threshold (prevent over-trading)
- Too many rebalances wastes gas → Keep delta higher
- Confidence decreases with failures

**DYNAMIC_HARVEST Strategy:**
- If success rate < 60% → Lower gas ratio threshold
- If gas estimates wrong → Adjust multiplier
- Confidence based on actual vs estimated gas costs

### Example Output

```
🧠 Reinforced Learning Report
────────────────────────────────────────────

COMPOUND_YIELD STRATEGY
  Success Rate:   92.5%
  Threshold:      $22.50  (was $25, lowered by 10%)
  Confidence:     92.5%

REBALANCE STRATEGY
  Success Rate:   85.0%
  APR Delta:      2.1%    (was 2.0%, slightly increased)
  Confidence:     85.0%

DYNAMIC_HARVEST STRATEGY
  Success Rate:   88.3%
  Gas Ratio:      1.80    (was 2.0, lowered)
  Confidence:     88.3%

🚀 Recent Improvements
  1. [COMPOUND] Lowered threshold - capturing more smaller harvests
  2. [HARVEST] Adjusted gas ratio - more conservative estimates
```

### Code Integration

```javascript
const ReinforcedLearning = require('./reinforced-learning');

const learning = new ReinforcedLearning();

// Analyze history and get optimized config
const optimizedConfig = learning.learn();

// Use optimized parameters in strategy
const harvestThreshold = optimizedConfig.agent.harvest_threshold_usd;
const rebalanceDelta = optimizedConfig.agent.rebalance_apr_delta;

// View progress
learning.printReport();
```

---

## Performance Over Time

### What the System Tracks

1. **Execution History** (`execution-log.jsonl`)
   - Every action with timestamp, vault, rewards, TX hash
   - All errors with reasons

2. **Performance Metrics** (`performance-metrics.json`)
   - Cumulative harvested/compounded
   - Per-vault yields
   - Realized APR

3. **Learning State** (`learning-state.json`)
   - Strategy success rates
   - Optimized parameters
   - Confidence levels
   - Improvement history

### How to Interpret Performance

**Realized APR** = (Total Harvested ÷ Total Deposited) × 365 × 100
- Example: Harvested $100 from $1000 in 365 days = 10% APR

**Success Rate** = Successful Actions ÷ Total Actions
- Goal: > 90% success rate
- Learning system improves this automatically

**Confidence Level** = Based on success history per strategy
- Starts at 50%
- Increases toward 95% as strategy succeeds
- Decreases if errors occur

---

## Integration with Strategy Scheduler

The learning system runs automatically:

```javascript
// In strategy-scheduler.js
const ReinforcedLearning = require('./reinforced-learning');
const learning = new ReinforcedLearning();

// Every 100 cycles, learn and optimize
if (cycleNumber % 100 === 0) {
  const optimizedConfig = learning.learn();
  // Apply new parameters to engine
}
```

---

## Use Cases

### Testnet Development
```bash
# Start with testnet (low cost)
node agent-cli.js network testnet
node strategy-scheduler.js

# Monitor and optimize locally
node agent-cli.js perf report
node agent-cli.js learn now

# When confident, switch to mainnet
node agent-cli.js network mainnet
```

### Production Mainnet
```bash
# Higher thresholds for safety
node agent-cli.js network mainnet

# Run with learning enabled (auto-optimizes)
node strategy-scheduler.js

# Monitor performance weekly
node agent-cli.js perf report
node agent-cli.js learn now
```

### Real-Time Adjustment
```bash
# If strategies fail, quickly optimize
node agent-cli.js learn now

# Check if mainnet needs adjustment
node agent-cli.js network status

# View improvement suggestions
node agent-cli.js learn report
```

---

## Safety Features

### Testnet vs Mainnet Guardrails

| Feature | Testnet | Mainnet |
|---------|---------|---------|
| Harvest Min | $25 | $100 |
| Gas Multiplier | 1.2x | 1.5x |
| Max Rebalance | No limit | Conservative |
| TX Timeout | 120s | 300s |

### Failure Prevention

- ✅ Gas estimates use multiplier (1.2-1.5x)
- ✅ Learning reduces risky operations
- ✅ Confidence thresholds prevent low-confidence trades
- ✅ Error logging for audit trail
- ✅ Graceful degradation (skip bad cycles)

---

## Troubleshooting

### Learning Isn't Helping?

```bash
# Check learning state
cat learning-state.json | jq

# Reset if corrupted
node agent-cli.js learn reset

# Analyze what's failing
node agent-cli.js perf report
```

### Network Switching Issues?

```bash
# Verify current network
node agent-cli.js network status

# Check saved preference
cat .network.json

# Manually switch
node agent-cli.js network testnet
```

### Performance Metrics Wrong?

```bash
# Recount from logs
node agent-cli.js perf summary

# Check log integrity
tail execution-log.jsonl | jq
```

---

## Summary

| Feature | Status | Usage |
|---------|--------|-------|
| **Network Switcher** | ✅ Complete | `network {testnet\|mainnet}` |
| **Performance Analytics** | ✅ Complete | `perf {summary\|report\|vaults\|strategies}` |
| **Reinforced Learning** | ✅ Complete | `learn {now\|report\|reset}` |
| **Auto-Optimization** | ✅ Complete | Runs every 100 cycles |
| **Safety Guardrails** | ✅ Complete | Per-network configuration |

All requested features are **production-ready** and **actively learning**! 🚀

---

**Last Updated**: 2026-02-18  
**Version**: 1.1.0  
**Status**: Ready for Mainnet Deployment
