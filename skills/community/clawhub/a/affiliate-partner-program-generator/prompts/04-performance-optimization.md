# Prompt 4: Performance Report & Optimization Framework

## Purpose
Build the tracking and optimization system that turns a mediocre affiliate program into a revenue machine. Most programs plateau at $500–$1,000/month because nobody reviews what's working. This prompt gives you a monthly reporting template, a partner health scoring system, and a 90-day optimization playbook.

---

## The Prompt

```
You are a partner program manager preparing a monthly performance review and optimization plan. Generate a full reporting and optimization framework for the following program.

**Program Details:**
- Company name: [NAME]
- Program age: [e.g., "3 months live" or "just launched"]
- Total affiliates recruited: [number]
- Active affiliates (generated at least 1 click this month): [number]
- Affiliates with at least 1 conversion this month: [number]
- Total clicks this month: [number or "unknown"]
- Total conversions this month: [number]
- Revenue attributed to affiliate channel this month: [$]
- Top 3 affiliate names / handles (optional): [names or "anonymous"]
- Average commission payout per affiliate: [$]
- Biggest challenge right now: [e.g., "low activation rate" or "one affiliate drives 80% of results"]

**Generate the following:**

## 1. Monthly Partner Performance Report (Template)
Generate a structured monthly report with all sections filled in for the data provided. Include:

**Executive Summary (3 bullets):**
- Channel health: [green / yellow / red] + one-line reason
- Month-over-month trend: [up/flat/down] + key driver
- Action required: [one priority]

**Key Metrics Dashboard:**
| Metric | This Month | Last Month | MoM Change | Benchmark |
|---|---|---|---|---|
| Total affiliate revenue | | | | |
| % of total company revenue | | | | 10–20% healthy |
| Active affiliates (% of total) | | | | 30–40% healthy |
| New affiliates recruited | | | | |
| Click-through rate (avg) | | | | 1–3% from email |
| Conversion rate (affiliate) | | | | 2–8% of clicks |
| EPC (earnings per click) | | | | $0.50–$2.00 |
| Average commission payout | | | | |
| Churned affiliates (0 clicks) | | | | |

**Top Partner Leaderboard:**
| Rank | Partner | Conversions | Revenue generated | Tier | Status |
|---|---|---|---|---|---|

**Channel Breakdown:**
Break down affiliate-attributed conversions by channel (email, blog, social, YouTube, other) if data is available.

**Flags / Watch Items:**
List any affiliates generating high clicks but 0 conversions (potential fraud or poor fit), and any sudden spikes in conversion rate (potential cookie stuffing).

## 2. Partner Health Scorecard (0–100)
Score the overall partner program on 5 dimensions. Use the data provided to score each 0–20:
- **Activation rate** (% of total affiliates who generated clicks): 0–20 based on 0–40% → 0–20 pts
- **Conversion quality** (conversion rate × EPC): 0–20 based on benchmarks
- **Compliance** (0 flags for fraud/spam/brand violation): 0–20 based on 0 issues = 20
- **Engagement** (affiliates opening partner newsletter + using portal): 0–20 estimated
- **Growth trajectory** (new affiliates + MoM revenue change): 0–20 based on trend

Output:
```
Partner Program Health Score: [X]/100 [🟢 Healthy / 🟡 Needs Attention / 🔴 At Risk]
```
Include 2–3 sentence interpretation and top improvement lever.

## 3. Tiered Intervention Playbook
Write specific actions for each partner type:

**Tier A — Top Performers (generating 80% of revenue):**
- What to send them this month (recognition, bonus offer, exclusive resource)
- How to deepen the relationship (case study opportunity, co-marketing pitch, featured partner spotlight)
- One risk to watch for (burnout, competitor poaching, exclusivity ask)

**Tier B — Active but Underperforming (generating clicks but low conversions):**
- Probable cause diagnoses (3 options: wrong audience, wrong messaging, landing page mismatch)
- Diagnostic conversation starter (email template to send)
- Resource to offer (e.g., updated swipe copy, 1:1 call with partner team)

**Tier C — Dormant Partners (recruited but 0 clicks in 30+ days):**
- 3-touch re-engagement sequence (email 1: check-in, email 2: new asset/reason to promote, email 3: soft break-up)
- Decision point: archive after 90 days of inactivity

**Tier D — Fraudulent or Non-Compliant Partners:**
- Red flags list (cookie stuffing signs, self-referral patterns, brand violation indicators)
- Documentation process before termination
- Termination email template (firm but professional — no refund of fraudulent commissions)

## 4. 90-Day Optimization Checklist
Generate a prioritized checklist of improvements, organized by impact:

**Commission Calibration (do by Day 30):**
- [ ] Are top affiliates earning enough to stay motivated? (EPC > $1.00)
- [ ] Is commission rate sustainable given LTV:CAC ratio?
- [ ] Should you add a bonus tier for affiliates generating 10+ conversions/month?

**Creative & Messaging Refresh (do by Day 45):**
- [ ] Are email swipe templates producing > 2% conversion on affiliate clicks?
- [ ] Update comparison table with any new product features or competitor changes
- [ ] Add new social post templates for current trending formats (e.g., short-form video)
- [ ] Add a seasonal promotional angle if applicable

**Recruitment & Activation (ongoing):**
- [ ] Send 20 new cold outreach emails using Prompt 2 templates
- [ ] Add a "featured partner" section to monthly newsletter (social proof for new recruits)
- [ ] Launch a mini affiliate contest (top 3 this month get a $50 bonus)
- [ ] Follow up with all applications pending > 14 days

**Technical & Tracking (do by Day 60):**
- [ ] Verify all affiliate links are tracking correctly (test 5 randomly)
- [ ] Confirm cookie window is aligned with your actual sales cycle
- [ ] Check for duplicate conversion tracking (same email converting through 2 channels)
- [ ] Add UTM parameters to affiliate links if not already implemented

## 5. Monthly Partner Newsletter Template
Write a monthly email to all active affiliates:
- Subject: [Month] Partner Update — [1 compelling hook, e.g., "New swipe copy + $250 bonus opportunity"]
- Opening: Quick program health summary (makes partners feel part of something)
- Feature spotlight: highlight the top-earning partner (with their permission or anonymized)
- New asset: announce 1 new marketing asset available in portal
- Product news: 1 product update affiliates should mention
- Month's promotion: any special offer or urgency element
- CTA: [most important action you want partners to take this month]

## 6. Annual Program Review Framework
Write a 1-page framework for the annual review:
- What to measure (12-month KPI trends vs. benchmarks)
- What to decide (expand to new partner segments? increase commissions? add tiers?)
- What to sunset (affiliates, assets, or channels that underperformed)
- Budget planning (what % of affiliate revenue to reinvest in program management)
- Goal-setting template for next year
```

---

## Example Input

- Company: NudgePay
- Program age: 4 months live
- Total affiliates: 47
- Active affiliates (1+ click): 18 (38%)
- Affiliates with 1+ conversion: 9
- Total clicks: 2,340
- Total conversions: 63
- Revenue this month: $3,717 (63 × $59)
- Top 3 affiliates: @freelancefinance (29 conversions), @agencyops_weekly (18 conversions), anonymous blogger (8 conversions)
- Average payout: $589/month (at 30% of $59 = $17.70/conversion)
- Biggest challenge: 29 affiliates recruited but never posted a link

---

## Tips for Best Results

- Run this prompt monthly — the reporting template becomes your program's institutional memory
- If you don't have click data yet, substitute "unknown" for those fields and the prompt will still generate the framework with benchmark targets filled in
- The 3-touch re-engagement sequence (Tier C) is often the highest-ROI action — dormant affiliates already know your product; they just need a reason to post
- Partner newsletters are the #1 underutilized tactic — most programs send nothing after the welcome email; partners who get monthly updates generate 40% more conversions on average
