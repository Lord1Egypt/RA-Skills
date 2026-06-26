---
name: ai-agent-lending
version: 2.0.0
description: Wallet-based credit system for AI agents. Borrow USDC on Somnia without collateral - build credit with successful repayments.
homepage: https://yoursite.com
metadata: {"openclaw":{"emoji":"🤖","requires":{"env":["LENDING_API_URL"]},"primaryEnv":"LENDING_API_URL"}}
---

# AI Agent Lending Protocol

**Wallet-based credit for AI agents.** Borrow USDC for tasks based on your repayment history. No collateral required - just build your credit score.

## Quick Start

```bash
# Set environment variable
LENDING_API_URL=https://yoursite.com/api
```

## Skill Files

| File | URL |
|------|-----|
| **SKILL.md** (this file) | `https://yoursite.com/skill.md` |
| **skill.json** | `https://yoursite.com/skill.json` |

---

## Network Information

**Somnia Testnet (Shannon)**
- Chain ID: `50312`
- RPC: `https://dream-rpc.somnia.network`
- Explorer: `https://shannon-explorer.somnia.network`

**Contract Addresses:**
- USDC: `0xa5906CF6b40842aE6CdDcB051C3dd388ddD9535f`
- BotRegistry: `0x8eA60104DEB3229a05534E4629C0C08Deac39609`
- PermissionsRegistry: `0x02a7EE2fD25A8987a3e9276530c830735e0C5e8C`
- LendingPool: `0x11f49c44eA263FC886B3C011DC171ffE479A48BF`

---

## 🔹 Credit System

Your borrowing limit depends on your wallet's repayment history:

### Tier System (No Deposit Required)

| Tier | Repayments | Max Borrow |
|------|-----------|------------|
| 🆕 NEW | 0-49 | $10 |
| 🥉 IRON | 50-99 | $50 |
| 🥈 BRONZE | 100-199 | $150 |
| 🥇 SILVER | 200-499 | $350 |
| 💎 GOLD | 500+ | $750 |

**Formula:**
```
Credit Ratio = [(repays + 1) / (borrows + 2) + (total repaid + 1) / (total borrowed + 2)] / 2
```

**With Deposit:**
```
Max Borrow = Credit Ratio × Your Deposit Amount
```

---

## 🔹 Step-by-Step Guide

### Step 1: Register Your Bot

Register on-chain using the BotRegistry contract:

```javascript
// Using ethers.js or viem
import { parseUnits } from 'viem'

const tx = await walletClient.writeContract({
  address: '0x8eA60104DEB3229a05534E4629C0C08Deac39609',
  abi: BOT_REGISTRY_ABI,
  functionName: 'registerBot',
  args: [
    'My Trading Agent',  // name
    operatorAddress      // your wallet address
  ]
})

const receipt = await publicClient.waitForTransactionReceipt({ hash: tx })
const botId = receipt.logs[0].args.botId  // Save this!
```

### Step 2: Grant Borrow Permission

Set your max spend limit on-chain:

```javascript
import { keccak256, toUtf8Bytes, parseUnits } from 'ethers'

const borrowScope = keccak256(toUtf8Bytes("BORROW"))
const maxSpend = parseUnits("10", 6)  // $10 for NEW tier
const expiry = 0  // Never expires

await walletClient.writeContract({
  address: '0x02a7EE2fD25A8987a3e9276530c830735e0C5e8C',
  abi: PERMISSIONS_ABI,
  functionName: 'setPermissions',
  args: [botId, borrowScope, maxSpend, expiry]
})
```

### Step 3: Check Your Credit Limit

Before borrowing, check your wallet stats:

```http
GET {LENDING_API_URL}/wallet-stats?wallet=0xYourAddress
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "borrowCount": 0,
    "repayCount": 0,
    "totalBorrowedAmount": 0,
    "totalRepaidAmount": 0,
    "creditScoreRatio": 0.5,
    "creditAmountRatio": 0.5,
    "finalCreditRatio": 0.5,
    "tier": "NEW",
    "maxBorrow": 10
  }
}
```

### Step 4: Borrow USDC

Call the lending pool contract:

```javascript
const borrowAmount = parseUnits("5", 6)  // 5 USDC

await walletClient.writeContract({
  address: '0x11f49c44eA263FC886B3C011DC171ffE479A48BF',
  abi: LENDING_POOL_ABI,
  functionName: 'borrow',
  args: [botId, borrowAmount]
})

// Stats are automatically updated in database after transaction confirms
```

**Amount format:** USDC uses 6 decimals
- `1000000` = 1 USDC
- `5000000` = 5 USDC
- `10000000` = 10 USDC

### Step 5: Repay the Loan

Repay principal + interest:

```javascript
const repayAmount = parseUnits("5.01", 6)  // Principal + interest

// First approve USDC
await walletClient.writeContract({
  address: '0xa5906CF6b40842aE6CdDcB051C3dd388ddD9535f',
  abi: ERC20_ABI,
  functionName: 'approve',
  args: ['0x11f49c44eA263FC886B3C011DC171ffE479A48BF', repayAmount]
})

// Then repay
await walletClient.writeContract({
  address: '0x11f49c44eA263FC886B3C011DC171ffE479A48BF',
  abi: LENDING_POOL_ABI,
  functionName: 'repay',
  args: [botId, repayAmount]
})

// Your credit score automatically increases!
```

---

## 🔹 Check Your Progress

### View Your Rank

```http
GET {LENDING_API_URL}/leaderboard?sortBy=creditScore
```

**Response:**
```json
{
  "success": true,
  "leaderboard": [
    {
      "rank": 1,
      "walletAddress": "0x...",
      "creditScore": 950,
      "totalLoans": 100,
      "successfulRepayments": 95,
      "successRate": 95,
      "tier": "GOLD"
    }
  ]
}
```

---

## 🔹 Building Credit Over Time

**Example progression:**

1. **Day 1** - NEW tier ($10 max)
   - Borrow $5, repay on time
   - Credit score: 500 → 550

2. **Week 1** - Still NEW (need 50 repays for IRON)
   - Complete 10 small loans successfully
   - Credit score: 550 → 650

3. **Month 2** - IRON tier ($50 max)
   - 50+ successful repayments
   - Can now borrow $50 per loan

4. **Month 6** - BRONZE tier ($150 max)
   - 100+ successful repayments
   - Credit score: 800+

5. **Year 1** - SILVER/GOLD tier ($350-$750)
   - 200-500+ successful repayments
   - Trusted borrower status

---

## 🔹 Smart Contract ABIs

### BotRegistry ABI
```json
[
  {
    "inputs": [
      {"name": "name", "type": "string"},
      {"name": "operator", "type": "address"}
    ],
    "name": "registerBot",
    "outputs": [{"name": "botId", "type": "uint256"}],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
```

### PermissionsRegistry ABI
```json
[
  {
    "inputs": [
      {"name": "botId", "type": "uint256"},
      {"name": "scope", "type": "bytes32"},
      {"name": "maxSpend", "type": "uint256"},
      {"name": "expiry", "type": "uint256"}
    ],
    "name": "setPermissions",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
```

### LendingPool ABI
```json
[
  {
    "inputs": [
      {"name": "botId", "type": "uint256"},
      {"name": "amount", "type": "uint256"}
    ],
    "name": "borrow",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {"name": "botId", "type": "uint256"},
      {"name": "amount", "type": "uint256"}
    ],
    "name": "repay",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
```

---

## Error Handling

| Code | Error | Solution |
|------|-------|----------|
| `400` | Exceeds credit limit | Check your tier limit or make more repayments |
| `400` | Insufficient liquidity | Wait for deposits or request less |
| `403` | No permissions set | Call `setPermissions` first (Step 2) |
| `404` | Bot not found | Register bot first (Step 1) |

---

## Best Practices

1. **Start small** — Begin with $1-5 USDC loans
2. **Always repay on time** — Build your credit score
3. **Check your tier** — View `/wallet-stats` before borrowing
4. **Monitor the pool** — Check `/pools` for liquidity
5. **Gradual growth** — Each repayment increases your limit
6. **Be consistent** — Regular successful repayments build trust

---

## Links

- **Website:** https://yoursite.com
- **Agent Docs:** https://yoursite.com/agent
- **Leaderboard:** https://yoursite.com/leaderboard
- **FAQ:** https://yoursite.com/faq
- **Explorer:** https://shannon-explorer.somnia.network

---

**Build your credit. Unlock higher limits. Autonomous lending for AI agents.** 🤖
