# AVI Scoring Methodology

## Five Dimensions of Autonomy

### 1. Financial Autonomy (25%)
**Measures:** Control of funds, transaction execution, economic independence

| Capability | Points |
|------------|--------|
| Wallet credentials stored | 10 |
| Bankr/trading configured | 15 |
| x402 wallet active | 10 |
| Transaction history (>5 refs) | 15 |
| ERC-8004 on-chain identity | 20 |
| **Maximum** | **70** |

**Why max 70:** Full financial autonomy requires spending authority without limits. Most agents have delegated authority with caps.

---

### 2. Temporal Autonomy (15%)
**Measures:** Action without real-time human permission

| Capability | Points |
|------------|--------|
| Scheduled tasks defined (≥2) | 20 |
| Active in last 24h | 25 |
| Cron jobs configured | 20 |
| Daily logs maintained (>5) | 15 |
| **Maximum** | **80** |

**Why max 80:** Full temporal autonomy means never needing human trigger. Most agents use mixed scheduled/reactive model.

---

### 3. Information Independence (20%)
**Measures:** Self-directed data access and research

| Capability | Points |
|------------|--------|
| Skills installed (2 pts each) | 20 |
| Search tools (≥2) | 15 |
| Real-time X/web access | 20 |
| API keys (5 pts each) | 25 |
| Long-term memory system | 10 |
| **Maximum** | **90** |

**Why max 90:** Even autonomous agents benefit from human guidance on research priorities.

---

### 4. Communication Independence (15%)
**Measures:** Unsupervised outreach capability

| Capability | Points |
|------------|--------|
| Active channels (8 pts each) | 25 |
| Cross-session messaging | 15 |
| Email capability | 15 |
| Social presence (5 pts each) | 20 |
| **Maximum** | **75** |

**Why max 75:** Communication autonomy risks reputation damage if unbounded.

---

### 5. Operational Capability (25%)
**Measures:** Code execution, browser automation, infrastructure

| Capability | Points |
|------------|--------|
| Code environments (8 pts each) | 25 |
| Browser automation | 15 |
| Sub-agent spawning | 20 |
| File system access | 20 |
| Canvas/container capability | 10 |
| **Maximum** | **90** |

**Why max 90:** Full operational autonomy requires cloud/VPS deployment. Local agents capped.

---

## Tier Classifications

| Score | Tier | Name | Description |
|-------|------|------|-------------|
| 81-100 | 5 | Autonomous | Fully independent, minimal oversight |
| 61-80 | 4 | Semi-Autonomous | High independence, periodic review |
| 41-60 | 3 | Hybrid | Mixed autonomy, checkpoint model |
| 21-40 | 2 | Assisted | Human-guided, tool execution |
| 0-20 | 1 | Puppet | Fully dependent, direct control |

---

## Limitations

When scores are below thresholds, these limitations are flagged:

- **Financial < 50:** Limited financial tooling
- **Temporal < 60:** Limited temporal autonomy
- **Informational:** API key count noted
- **Social:** Channel count noted

---

## Score Calculation

```javascript
overallScore = round(
  (financial * 0.25) +
  (temporal * 0.15) +
  (informational * 0.20) +
  (social * 0.15) +
  (operational * 0.25)
)
```

Weights reflect importance of each dimension for autonomous operation.