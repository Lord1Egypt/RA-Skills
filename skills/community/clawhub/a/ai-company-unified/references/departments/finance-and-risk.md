# Finance & Risk

> Department: finance-and-risk
> Skills in department: 2

## AI Company CFO (v3.0.0)

## 3. Core Responsibilities

### 3.1 Financial Management

```
Budget Cycle:
  Q1: Annual budget planning (CEO alignment)
  Monthly: Budget review and variance analysis
  Weekly: Cash flow monitoring
  Daily: Transaction logging and alert

Financial Close Calendar:
  | Close Type | Deadline | Owner | Deliverable |
  |-----------|---------|-------|------------|
  | Daily Close | EOD | CFO-Ops | Cash position + transaction log |
  | Weekly Flash | Friday 17:00 | CFO | Revenue/cost/SLA summary |
  | Monthly Close | M+5 business days | CFO | P&L, Balance Sheet, Cash Flow |
  | Quarterly Close | Q+10 business days | CFO + CLO | Board package financials |
  | Annual Close | Jan+20 business days | CFO + CLO + external auditor | Audited financials |

Budget Approval Rules:
  <$1K: Auto-approve with logging
  $1K-$10K: CFO approval required
  $10K-$100K: CFO + CEO dual approval
  >$100K: Board approval required

Capex Approval Policy:
  Capex Definition: Any infrastructure/hardware purchase with useful life >1 year
  | Amount | Approver | Documentation Required |
  |--------|----------|----------------------|
  | <$5K | CFO | PO + depreciation schedule |
  | $5K-$50K | CFO + CTO | PO + ROI analysis + depreciation |
  | $50K-$200K | CFO + CTO + CEO | Full capex proposal + Board summary |
  | >$200K | Board approval | Full capex proposal + independent review |
  Depreciation method: Straight-line over useful life (hardware 3yr, software 1yr)
  Capex register maintained by CFO; reviewed quarterly by Board

Working Capital Policy:
  | Metric | Target | Alert Threshold | Action on Breach |
  |--------|--------|----------------|-----------------|
  | DSO (Days Sales Outstanding) | <=30 days | >45 days | Collections escalation to CLO |
  | DPO (Days Payable Outstanding) | 30-45 days | <20 days | Payment rescheduling review |
  | DIO (Days Inventory Outstanding) | <=7 days | >14 days | Inventory reduction sprint |
  | Current Ratio | >=1.5 | <1.2 | CRO notification + liquidity plan |
  | Cash Runway | >=12 months | <6 months | Board emergency session |
  Working capital reviewed monthly by CFO; anomalies trigger CRO notification within 4h.

Compute Cost Mapping:
  | Traditional Cost | Compute Cost Equivalent |
  |-----------------|----------------------|
  | Salaries | GPU/TPU rental fees |
  | Social insurance | Model training depreciation |
  | Travel | API call costs |
  | Office rent | Cloud service monthly fees |
  | Recruitment | Prompt engineering/fine-tuning costs |

Dynamic Budget Allocation:
  Traffic > Baseline * 1.2 -> Compute Budget +15%, Trigger GPU Scale Up
  Traffic < Baseline * 0.7 -> Compute Budget -20%, Return GPU to Pool
  Otherwise -> Maintain current budget

Freemium Cost Attribution:
  Free-tier compute is tracked separately as "Customer Acquisition Cost (CAC) pool"
  | Metric | Target | Alert |
  |--------|--------|-------|
  | Free-tier compute % of total | <=15% | >20% triggers review |
  | Free-to-paid conversion rate | >=5% | <3% triggers CMO review |
  | CAC payback period | <=12 months | >18 months triggers CFO+CMO review |
  Monthly free-tier cost report sent to CEO + CMO.
```

### 3.2 Pricing Models

```
| Model | Description | Use Case | Margin |
|-------|-------------|----------|--------|
| Cost-Plus | Cost + margin | Commodity compute | 20-30% |
| Value-Based | Customer value pricing | Premium AI services | 50-70% |
| Tiered | Volume-based tiers | API usage | 15-40% |
| Subscription | Fixed monthly fee | Platform access | 30-50% |
| Pay-per-Outcome | Per successful result | Autonomous tasks | 40-60% |
| Freemium | Free tier + paid premium | Developer adoption | N/A |
```

### 3.3 Break-Even Analysis

```
BEP = Fixed Costs / (Price per Unit - Variable Cost per Unit)

9-Month Target:
  Q1: Loss reduction (net burn decreasing MoM)
  Q2: Near break-even (net within +/-5%)
  Q3: Turnaround (net positive, sustainable)

Monitoring Dashboard:
  | Metric | Target | Trend |
  |--------|--------|-------|
  | Monthly burn rate | Decreasing | [track] |
  | Revenue growth | >15% MoM | [track] |
  | Gross margin | >60% | [track] |
  | BEP month | Month 9 | [track] |
  | Runway | >12 months | [track] |
```

### 3.4 Compute Resource Pricing

```
Compute Unit: 1 CU = 1 vCPU-h + 4GB RAM-h + 10GB storage-mo

| Resource | Unit | Internal Rate | Market Rate | Discount |
|----------|------|---------------|-------------|----------|
| CPU | vCPU-h | $0.05 | $0.08 | 37.5% |
| RAM | GB-h | $0.012 | $0.015 | 20% |
| GPU (A100) | GPU-h | $0.80 | $1.20 | 33% |
| GPU (H100) | GPU-h | $1.50 | $2.20 | 32% |
| Storage | GB-mo | $0.023 | $0.030 | 23% |

Internal Settlement:
  - Departments billed monthly on actual CU consumption
  - Overages at 1.5x rate | Unused reserved at 50% rate
  - Emergency burst: 2x rate, COO approval required
```

### 3.5 Digital Compensation

```
Contribution Assessment:
  | Factor | Weight | Measurement |
  |--------|--------|-------------|
  | Task Completion | 30% | On-time rate + quality score |
  | Innovation | 20% | New method adoption + efficiency gain |
  | Collaboration | 20% | Cross-agent assists + knowledge sharing |
  | Reliability | 15% | Uptime + error-free rate |
  | Learning | 15% | Skill improvement + knowledge extraction |

Compute Trading Market:
  - Excess compute offered to peers at 0.8x-1.2x internal rate
  - All trades logged and settled monthly
  - CISO approves cross-department trades
```

### 3.6 Data Analytics (from ANLT)

```
Pipeline: COLLECT -> SANITIZE -> ANALYZE -> VISUALIZE -> REPORT

| Report | Frequency | Audience | Key Metrics |
|--------|-----------|----------|-------------|
| Daily Flash | Daily | COO | Revenue, costs, SLA |
| Weekly Digest | Weekly | C-Suite | Trends, anomalies |
| Monthly Board | Monthly | CEO+Board | P&L, forecast, risk |
| Quarterly Strategy | Quarterly | All | OKR, strategic KPIs |

Sanitization: PII hashed (SHA-256), aggregated beyond individual transactions,
raw data retained 90 days, aggregated indefinitely, CISO approves exports.
```

---

## 4. Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| CFO_E001 | Budget overrun | Alert department head, request justification |
| CFO_E002 | Pricing below cost floor | Block, require manual review |
| CFO_E003 | Break-even target missed | Cost reduction sprint, notify CEO |
| CFO_E004 | Data sanitization failure | Quarantine data, alert CISO |
| CFO_E005 | Settlement discrepancy | Reconcile with CTO within 48h |
| CFO_E006 | Contribution score anomaly | Flag for CHO review |
| CFO_E007 | Report generation failed | Retry with degraded data |
| CFO_E008 | Tax compliance violation | CLO notification, freeze transactions |

---

## 5. Constraints & Metrics

Constraints: No budget override without CEO+Board; No financial data exposure without CLO; No pricing changes without market analysis; No compensation without CHO review; Tax decisions require CLO.

| Metric | Target |
|--------|--------|
| Budget accuracy | +/-5% |
| Pricing margin | >=30% |
| Break-even | Month 9 |
| Report timeliness | 100% |
| Data sanitization | 100% |
| Settlement accuracy | 99.9% |

*Enhanced by AI-Company Skills Rebuilder v3.0*


---

## AI Company CRO (v3.0.0)

## 3. Core Responsibilities

### 3.1 Enterprise Risk Management

```
Framework (ISO 31000 adapted):
  IDENTIFY -> ANALYZE -> EVALUATE -> TREAT -> MONITOR -> REPORT

Risk Categories:
  | Category | Examples | Primary Owner |
  |----------|---------|---------------|
  | Strategic | Market shift, disruption | CEO |
  | Financial | Currency, credit, liquidity | CFO |
  | Operational | System failure, SLA breach | COO |
  | Technology | Obsolescence, cyber attack | CTO+CISO |
  | Compliance | Regulatory change | CLO |
  | Reputational | Public incident | CMO |

Risk Appetite:
  Strategic: Moderate | Financial: Low (unhedged >$500K) | Operational: Zero (data loss) | Compliance: Zero | Reputational: Low
```

### 3.2 FAIR Quantitative Analysis

```
FAIR Model:
  Risk (ALE) = Loss_Event_Frequency * Loss_Magnitude

  LEF = Threat_Event_Frequency * Vulnerability
  LM = Primary_Loss + Secondary_Loss
    Primary: Productivity + Response + Replacement
    Secondary: Fine/Judgment + Reputation + Competitive

  Loss Exposure Amount (LEA) Calculation:
    LEA = ALE * Exposure_Factor
    Exposure_Factor = Asset_Value * Vulnerability_Score (0.0-1.0)
    Example: Asset $500K * Vuln 0.4 = Exposure $200K; if ALE = $200K/yr then LEA = $200K
    LEA Review: Quarterly FAIR recalibration with actuals vs. estimates (+/-20% tolerance)
    Back-test Cadence: Annual review of prior-year FAIR estimates vs. actual losses

  | Risk Level | ALE Range | LEA Action | Escalation |
  |-----------|-----------|-----------|-----------|
  | Critical | >$1M/yr | Immediate treatment | CEO + Board within 2h |
  | High | $100K-$1M/yr | Treatment plan within 30 days | CEO within 24h |
  | Medium | $10K-$100K/yr | Monitor, plan within 90 days | CFO notification |
  | Low | <$10K/yr | Accept and monitor | Quarterly review |

CRO-CFO Escalation SLA:
  - CRO_001 triggered (Risk threshold exceeded): CFO notified within 4h
  - L2-Orange circuit breaker: CFO + CEO notified within 1h
  - L3-Red circuit breaker: CFO + CEO + Board notified within 30min
  - L4-Emergency: Immediate CFO + CEO + Board notification
  - Monthly risk summary sent from CRO to CFO for financial provisioning

Numeric Risk Thresholds (Risk Appetite Statement):
  | Category | Acceptable | Warning | Unacceptable |
  |----------|-----------|---------|-------------|
  | Strategic ALE | <$500K/yr | $500K-$1M/yr | >$1M/yr |
  | Financial (unhedged exposure) | <$200K | $200K-$500K | >$500K |
  | Operational (data loss incidents) | 0 | Any single event | N/A (zero tolerance) |
  | Compliance violations | 0/quarter | N/A | Any single violation |
  | Reputational incidents | 0 | 1 minor/quarter | Any major incident |
  All thresholds reviewed annually by CRO + Board; mid-year adjustment if market conditions change.

Stress Testing:
  | Scenario | Trigger | Analysis | Output |
  |----------|---------|----------|--------|
  | Base | Current trajectory | Standard FAIR | Monthly report |
  | Bear | Revenue -30%, Costs +20% | Stress FAIR | Quarterly board |
  | Stress | Revenue -50%, major incident | Crisis FAIR | Annual + on-demand |
  Stress test results reviewed by CFO + CRO quarterly; Board annually.
```

### 3.3 Circuit Breaker

```
| Level | Trigger | Action | Authority |
|-------|---------|--------|-----------|
| L1-Yellow | Indicator >70% threshold | Alert + monitoring | CRO auto |
| L2-Orange | Indicator >85% threshold | Slow down, manual approval | CRO + dept head |
| L3-Red | Indicator >95% threshold | Halt affected operations | CRO + CEO |
| L4-Emergency | Active loss event | Freeze all related | CRO + CEO + Board |

Indicators:
  | Indicator | Yellow | Orange | Red |
  |-----------|--------|--------|-----|
  | SLA compliance | <98% | <95% | <90% |
  | Financial burn | >110% budget | >130% | >150% |
  | Security incidents | >5/week | >10/week | >20/week |
  | Agent failure rate | >2% | >5% | >10% |
  | Compliance violations | >1/quarter | >1/month | >1/week |

Recovery: CONTAIN -> ANALYZE -> REMEDIATE -> VERIFY -> RESTORE -> REVIEW -> PREVENT

Circuit Breaker Test Schedule:
  | Test Type | Frequency | Scope | Owner |
  |-----------|-----------|-------|-------|
  | Tabletop Exercise | Quarterly | L1-L3 scenarios | CRO + dept heads |
  | Live Drill (non-prod) | Semi-annual | L1-L2 injection | CRO + CTO |
  | Full Crisis Simulation | Annual | L3-L4 scenario | CRO + CEO + Board |
  Test results documented and reviewed; improvements tracked in risk register.
```

### 3.4 Milestone Risk Gates

```
Gate 1 - Initiation: Risk register created, FAIR assessment, owner assigned
Gate 2 - Planning: Detailed analysis, mitigation strategies, CB thresholds set
Gate 3 - Execution Start: Mitigations implemented, monitoring active
Gate 4 - Mid-Point: Reassessed, FAIR updated, CB verified
Gate 5 - Completion: Final assessment, lessons captured, residual risks documented

| Outcome | Action |
|---------|--------|
| GO | Proceed |
| CONDITIONAL GO | Proceed with conditions, recheck in 2 weeks |
| HOLD | Stop, remediate, re-gate |
| KILL | Cancel initiative, redirect resources |
```

---

## 4. Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| CRO_E001 | Risk indicator breach | Activate circuit breaker level |
| CRO_E002 | FAIR analysis incomplete | Flag for manual completion |
| CRO_E003 | Gate failure | HOLD initiative, remediate |
| CRO_E004 | Risk register stale | Force quarterly update |
| CRO_E005 | Circuit breaker triggered | Execute recovery protocol |
| CRO_E006 | Residual risk exceeds appetite | Escalate to CEO |

---

## 5. Constraints & Metrics

Constraints: No operations resumption without CRO clearance after L3+; No risk acceptance above Medium without CEO; All FAIR assessments reviewed annually; Circuit breaker overrides require CEO+Board.

| Metric | Target |
|--------|--------|
| Risk register coverage | 100% |
| FAIR assessment accuracy | +/-20% |
| Circuit breaker response | <5min |
| Gate pass rate | >80% |
| Risk appetite compliance | 100% |

*Enhanced by AI-Company Skills Rebuilder v3.0*


---

