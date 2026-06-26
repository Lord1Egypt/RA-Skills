---
name: campaign-optimization
description: Expert playbook for Meta Ads campaign optimization decisions. Covers budget scaling, pausing, bid strategy selection, audience expansion, and ROAS improvement — specifically for Vietnamese ecommerce and retail advertisers.
---

# ⚡ Campaign Optimization Playbook

> **Purpose**: Make smart, data-driven optimization decisions. Every recommendation must cite specific metric evidence. Never optimize based on a single day's data.

---

## 1. Scaling Decision Rules

### 1.1 When to Scale Up (Increase Budget)
Conditions that MUST ALL be true:
```
✅ ROAS > 2.6 (scaleRoas threshold)
✅ Campaign NOT in Learning Phase (>50 conversions)
✅ At least 7 days of stable data
✅ Current budget is NOT exhausted (< 95% of daily budget spent)
✅ CTR (all) is stable or improving (not dropping week-over-week)
```

**How much to scale:**
- Conservative: +20% budget
- Standard: +30% budget
- Aggressive: +50% budget (only if ROAS > 3.5 AND 14+ days of data)

**Golden Rule**: Never more than +50% in a single step. Meta system needs time to adjust.

### 1.2 When to Scale Down (Decrease Budget)
Conditions (ANY ONE triggers review):
```
⚠️ ROAS < 1.5 for 3+ consecutive days
⚠️ CPA > 300,000đ (120% of 250,000đ threshold) for 3+ days
⚠️ CTR (all) dropped >40% week-over-week (creative fatigue)
⚠️ Budget utilization > 110% (overspending)
⚠️ Learning Limited status with no path to 50 conversions
```

**How much to reduce:**
- CPA slightly high: -20%
- CPA very high (>2x): -40%
- Not getting conversions: -50% or pause

### 1.3 When to PAUSE
```
🔴 CPA > 2x threshold (500,000đ+) for 5+ days
🔴 Zero conversions in 7 days with >1M VND spend
🔴 Ad account or payment method issue
🔴 Product out of stock / landing page down
```

---

## 2. Bid Strategy Decision Tree

```
Campaign Objective?
├── TRAFFIC / AWARENESS
│   → Highest volume
│   → No cost cap needed
│
└── CONVERSIONS / SALES
    ├── New campaign / testing phase?
    │   → Highest volume (let system learn first)
    │   → Wait for 50 conversions → then consider cost cap
    │
    └── Mature campaign (>50 conversions/week)?
        ├── CPA too volatile?
        │   → Cost per result goal: set at 110% of current CPA
        ├── ROAS inconsistent?
        │   → ROAS goal: set at 85% of target ROAS
        └── Competitive auction?
            → Bid cap: set at average CPC × 1.5 (estimate only)
```

---

## 3. Audience Strategy

### 3.1 Audience Size Guidelines (Vietnam market)
| Campaign Goal | Audience Size |
|--------------|---------------|
| Conversion (Purchase) | 500K – 3M |
| Lead Generation | 300K – 2M |
| Traffic / Retargeting | 50K – 500K |
| Broad (Advantage+) | Let Meta decide |

### 3.2 Audience Expansion Decision
**Expand when:**
- Frequency > 2.5 in 7 days (audience saturation)
- Reach is declining while budget is stable
- CTR (all) trending down with stable creative

**How to expand:**
1. Increase age range by ±5 years
2. Add 2–3 related interests
3. Switch to Advantage+ Audience (let Meta find similar accounts)
4. Move from detailed targeting → Broad targeting (Meta's recommendation for conversion objectives)

### 3.3 Audience Overlap Warning
- If 2+ ad sets target same audience → Auction overlap risk
- Signal: ad sets spending less than allocated budget despite being active
- Fix: Combine similar ad sets OR exclude overlapping audiences

---

## 4. Landing Page Optimization Rules

These are NOT Meta Ads issues but affect conversion rate ranking:

### High Conversion Rate Ranking Signals:
- Page load < 3 seconds (mobile)
- Offer on landing page MATCHES ad offer exactly
- Single clear CTA button visible above fold
- Social proof visible without scrolling

### Diagnose Landing Page Issues:
```
Low Conversion Rate Ranking + High CTR (link click-through rate)
  → People click but don't convert
  → Root cause: landing page mismatch OR slow load
  → Action: Check landing page on mobile, compare ad promise vs page
```

---

## 5. Campaign Health Scoring

Score each campaign out of 100:

| Metric | Green (full points) | Yellow (half) | Red (0) |
|--------|---------------------|---------------|---------|
| ROAS (20pt) | > 2.6 | 1.5–2.6 | < 1.5 |
| CPA (20pt) | < 200K | 200–250K | > 250K |
| CTR (all) (20pt) | > 2% | 1–2% | < 1% |
| Learning Phase (20pt) | Active learner | Learning Limited | — |
| Delivery (20pt) | Consistent spend | Under-delivery | Paused/Error |

**Score Interpretation:**
- **80–100**: 🟢 Scale this campaign
- **60–79**: 🟡 Monitor, optimize one variable
- **40–59**: 🟠 Needs significant intervention
- **< 40**: 🔴 Propose pause, reallocate budget

---

## 6. Budget Reallocation Framework

When one campaign is losing and another is winning:

```
Step 1: Identify loser (CPA > threshold, ROAS < 1.5)
Step 2: Identify winner (ROAS > 2.6, stable learning)
Step 3: Reduce loser by 30–40%
Step 4: Increase winner by equivalent VND amount
Step 5: Create proposal for boss approval
Step 6: Monitor for 3 days after change
```

**Budget reallocation example:**
```
Loser campaign: 500K/day → 300K/day (save 200K)
Winner campaign: 800K/day → 1,000K/day (add 200K)
Net: Same total spend, better ROAS mix
```

---

## 7. Weekly Optimization Checklist

Every 7 days, run through this checklist:

```
□ Review all campaigns: health score each one
□ Check learning phase status — any "Learning Limited"?
□ Review Engagement Rate Ranking — any drops to Below Average?
□ Check Creative Fatigue — frequency > 2.5 anywhere?
□ Review audience overlap — any ad sets underspending?
□ Check competitor memory — any new competitor data to analyze?
□ Create/update proposals for needed changes
□ Review and acknowledge any boss instructions
```

---

## 8. Vietnamese Market Seasonality Notes

High competition periods (budget more competitive, CPM spikes):
- **Tết Nguyên Đán** (Jan–Feb): CPM +50–100%, start campaigns early in Dec
- **8/3** (Women's Day): Beauty/fashion spike, 1–2 weeks before
- **11/11, 12/12**: Ecommerce sale events, prepare 2 weeks ahead
- **Ngày Gia Đình** (28/6): Family products spike
- **Back to School** (Aug): Education services spike

Low competition periods (cheaper CPM):
- February (post-Tết slump)
- June–July (summer low)

**Strategy**: Increase budget 2 weeks BEFORE high-competition events. Reduce during peak to ride organic demand if budget-constrained.
