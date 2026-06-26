# Performance Metrics & Optimization Cycles

## Core ASA Metrics

### Tap Through Rate (TTR)
**What it measures**: Ad engagement — what % of users who see your ad actually tap it.

**Formula**: Taps ÷ Impressions × 100

**Targets**:
- Minimum acceptable: 3%
- Good: 5-8%
- Excellent: 10%+

**Why it matters**: Low TTR means users are seeing your ad and ignoring it. Your app name, icon, or rating is failing to compete against adjacent results.

**Fix low TTR**:
1. Check app icon — does it stand out in search results?
2. Check star rating — below 4.0 dramatically reduces TTR
3. Check if your keyword match is actually relevant (users searching for X see your Y)
4. Consider custom product pages for specific keyword groups

---

### Conversion Rate (CR)
**What it measures**: What % of users who tap your ad actually install.

**Formula**: Installs ÷ Taps × 100

**Targets**:
- Minimum acceptable: 25%
- Good: 40-50%
- Excellent: 60%+

**Why it matters**: Low CR means users tap your ad, visit your product page, and leave without installing. The page is failing to convert intent into action.

**Fix low CR**:
1. First screenshot — does it communicate value in < 2 seconds?
2. App description hook — first 167 characters are visible without scrolling
3. Rating/review volume — fewer than 50 reviews hurts conversion
4. Keyword-to-product alignment — if your keyword promises something your app doesn't deliver, CR suffers

---

### Cost Per Tap (CPT)
**What it measures**: Average cost for each user who taps your ad.

**Formula**: Total Spend ÷ Taps

**Benchmarks by category** (broad ranges):
- Games: $0.30–$0.80
- Productivity: $0.50–$1.50
- Health/Fitness: $0.60–$1.80
- Finance: $1.00–$3.00

**Context**: CPT alone is meaningless — a $2.00 CPT with 60% CR is better than a $0.50 CPT with 10% CR.

---

### Cost Per Acquisition (CPA)
**What it measures**: Total cost per install.

**Formula**: Total Spend ÷ Installs (or CPT ÷ CR)

**This is your primary optimization target.**

**CPA trend analysis**:
- CPA rising week-over-week: keyword saturation, competition increasing, or CR declining
- CPA stable: healthy campaign
- CPA falling: positive signal — scale budget
- CPA spiking suddenly: bid change, competitor entered, seasonality, product page change

---

### Impression Share
**What it measures**: % of eligible auctions you actually win.

**Why it matters**: Low impression share on your best keywords = leaving installs on the table. High impression share = near saturation.

**Target**: 30-60% for generic keywords (full saturation is expensive). 70%+ acceptable for brand keywords.

---

## Daily, Weekly, Monthly Review Cadence

### Daily (5 minutes)
- Check total spend vs daily budget (pacing issue = budget too restrictive or CPA spiking)
- Flag any campaign with CPA > 2× target (investigate before it compounds)
- Check for any anomalies (sudden impression drop, spend stopping)

### Weekly (30 minutes)
- CPA trend vs target for each campaign
- TTR and CR trends — any declining campaigns
- Keyword performance: identify top 20% and bottom 20% performers
- Search terms export from Discovery campaign — add winners to exact match, losers to negatives
- Budget reallocation if one campaign is consistently under/over target

### Monthly (2 hours)
- Full keyword audit: pause underperformers, add new candidates
- Bid adjustment cycle based on month's data
- Cohort quality review — are ASA installs retaining and converting to paid?
- Budget reallocation across campaigns based on CPA trends
- Competitive landscape check — new competitors entering your keyword space?

---

## Diagnosing CPA Problems

### CPA Too High: Diagnostic Tree

```
CPA too high
├── TTR low (< 3%)
│   ├── Low ratings → fix product first
│   ├── Poor icon → ASO issue
│   └── Wrong keyword match → refine keywords
│
├── CR low (< 25%)
│   ├── Weak product page → screenshot/description optimization
│   ├── Keyword-product mismatch → better keyword selection
│   └── Poor rating → review management
│
└── CPT too high (winning auctions at inflated cost)
    ├── Bids too aggressive → reduce bids 15-20%
    ├── Highly competitive keyword → shift to long-tail
    └── Wrong campaign type for keyword → restructure
```

### CPA Too High: Quick Fixes (in order of impact)

1. Pause keywords with CPA > 3× target and 0 improvement trend
2. Shift budget from Competitor campaign to Generic (better baseline CR)
3. Add negative keywords to stop wasted taps
4. Reduce bids on low-CR keywords by 20%
5. Fix product page conversion issues (screenshots, rating)

---

## Cohort Quality Metrics (Beyond Install Count)

Installs are a proxy metric. What you actually want is **quality users**. Track these in your MMP or App Store Connect:

| Metric | What to track | Good benchmark |
|--------|--------------|----------------|
| Day 1 retention | % who return next day | > 30% |
| Day 7 retention | % who return after 1 week | > 15% |
| In-app conversion | % who complete key action | App-specific |
| Trial-to-paid | For subscription apps | > 20% |
| ARPU (30-day) | Revenue per acquired user | Depends on category |

**Why this matters for ASA**: If your generic campaign delivers 40% CR but 10% Day-1 retention, while your long-tail campaign delivers 30% CR but 35% Day-1 retention, the long-tail keywords are worth more — even at a higher CPA.

Break down cohort quality by campaign type. Often Competitor campaign installs have the worst retention (users who were loyal to a competitor). This justifies keeping Competitor campaign budgets modest.
