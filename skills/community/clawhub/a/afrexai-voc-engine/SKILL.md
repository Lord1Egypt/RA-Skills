---
name: afrexai-voc-engine
description: Complete Voice of Customer system — collect, analyze, and operationalize customer feedback at scale. Covers NPS/CSAT/CES measurement, customer interview methodology, feedback taxonomy, feature request prioritization, sentiment analysis, closed-loop workflows, and VoC-driven product decisions. Use when building feedback systems, running customer interviews, measuring satisfaction, analyzing feature requests, reducing churn, or closing the feedback loop. Trigger on "customer feedback", "voice of customer", "NPS", "CSAT", "CES", "feature requests", "feedback system", "customer interviews", "satisfaction survey", "churn analysis".
---

# Voice of Customer (VoC) Engine

Complete system for collecting, analyzing, and operationalizing customer feedback to drive product decisions, reduce churn, and increase expansion revenue.

---

## Phase 1: VoC Program Design

### Program Brief

```yaml
voc_program:
  company: "[Company Name]"
  product: "[Product/Service]"
  stage: "[Pre-PMF | Growth | Scale | Enterprise]"
  customer_count: "[approximate]"
  current_nps: "[score or unknown]"
  current_churn: "[monthly % or unknown]"
  primary_goal: "[reduce churn | improve NPS | prioritize roadmap | find PMF]"
  
  segments:
    - name: "[Enterprise / SMB / Consumer]"
      size: "[count]"
      arr_contribution: "[%]"
      priority: "[1-3]"
    
  existing_channels:
    - "[list current feedback collection methods]"
  
  gaps:
    - "[what feedback are you NOT collecting?]"
```

### VoC Maturity Assessment

Score your current program (1-5 per dimension):

| Dimension | 1 (Ad Hoc) | 3 (Structured) | 5 (Operationalized) |
|-----------|-----------|----------------|---------------------|
| **Collection** | Sporadic, reactive only | Multiple channels, some regularity | Automated, multi-channel, triggered |
| **Analysis** | Read individual comments | Tag and categorize | Quantified themes, trend tracking |
| **Distribution** | Stays with support team | Shared in meetings | Real-time dashboards, auto-routed |
| **Action** | Occasional fixes | Quarterly roadmap input | Closed-loop, feedback drives decisions |
| **Measurement** | No tracking | NPS or CSAT exists | Full metric suite, benchmarked |

**Score interpretation:**
- 5-10: Foundation needed — start with Phase 2 basics
- 11-18: Growing — focus on analysis and distribution
- 19-25: Mature — optimize closed-loop and ROI tracking

---

## Phase 2: Feedback Collection Architecture

### Channel Strategy

Design feedback collection around the customer journey:

```yaml
collection_channels:
  # ALWAYS-ON (continuous)
  in_app_widget:
    placement: "[specific screens/moments]"
    trigger: "User-initiated (feedback button)"
    format: "Open text + optional category selector"
    volume: "High"
    quality: "Medium (context-rich but brief)"
    
  support_tickets:
    source: "[Intercom / Zendesk / Help Scout / email]"
    tagging: "Auto-tag feedback themes (see taxonomy)"
    volume: "High"
    quality: "High (real problems, real context)"
    
  feature_request_board:
    tool: "[Canny / ProductBoard / custom]"
    voting: true
    status_updates: true  # Close the loop!
    volume: "Medium"
    quality: "High (considered requests)"

  # PERIODIC (scheduled)
  nps_survey:
    frequency: "Quarterly"
    trigger: "Email to active users (>30 days tenure)"
    follow_up: "Open text for score explanation"
    segments: "[by plan tier, tenure, usage level]"
    
  csat_survey:
    trigger: "After key interactions (onboarding complete, support resolved, feature shipped)"
    format: "1-5 stars + optional comment"
    
  ces_survey:
    trigger: "After task completion (setup, first report, integration)"
    question: "How easy was it to [specific task]? (1-7)"
    
  # EVENT-DRIVEN (triggered)
  onboarding_check_in:
    trigger: "Day 7, Day 30, Day 90"
    format: "Short email survey (3 questions max)"
    
  cancellation_survey:
    trigger: "On churn/downgrade"
    format: "Required reason + optional comment"
    options:
      - "Too expensive"
      - "Missing features I need"
      - "Too complex / hard to use"
      - "Switched to competitor"
      - "No longer need this type of product"
      - "Poor support experience"
      - "Other: [free text]"
    
  win_loss_interview:
    trigger: "After closed-won or closed-lost deal"
    format: "15-min call or async survey"
    
  renewal_feedback:
    trigger: "30 days before renewal"
    format: "Health check + satisfaction + roadmap preview"
```

### Survey Design Rules

1. **Max 3 questions** per survey (response rate drops 20% per additional question)
2. **One metric question + one open text** is the minimum viable survey
3. **Timing matters:** Send within 24 hours of the trigger event
4. **Mobile-first:** Design for thumb-scrolling
5. **Never survey angry:** Wait 48 hours after a negative support interaction
6. **Frequency cap:** No user gets surveyed more than once per quarter (except event-driven)
7. **Always explain why:** "Help us improve [specific thing]" > "Take our survey"

### Sample Size Calculator

| Customer Base | Confidence 95%, ±5% | Confidence 90%, ±5% | Minimum Viable |
|--------------|---------------------|---------------------|----------------|
| 100 | 80 | 74 | 30 |
| 500 | 217 | 176 | 50 |
| 1,000 | 278 | 213 | 75 |
| 5,000 | 357 | 258 | 100 |
| 10,000+ | 370 | 264 | 150 |

**Expected response rates by channel:**
- In-app: 10-15%
- Email NPS: 20-40%
- Post-support CSAT: 15-25%
- Cancellation: 30-50% (required = 80%+)

---

## Phase 3: Customer Interview Methodology

### Interview Types

| Type | When | Duration | Sample | Goal |
|------|------|----------|--------|------|
| **Discovery** | Pre-build, exploring problem | 45-60 min | 8-12 | Validate problem exists |
| **Usability** | Feature in development | 30-45 min | 5-7 | Test assumptions |
| **Satisfaction** | Ongoing, quarterly | 30 min | 5-8 per segment | Deep qualitative NPS |
| **Churn** | After cancellation | 15-20 min | All willing | Understand why they left |
| **Win/Loss** | After deal close | 20-30 min | 5+ per quarter | Sales process feedback |
| **Advisory** | Strategic, quarterly | 60 min | 3-5 power users | Co-create roadmap |

### Interview Guide Template

```yaml
interview:
  type: "[Discovery / Satisfaction / Churn / Win-Loss]"
  participant: "[name, role, company, segment]"
  date: "[YYYY-MM-DD]"
  interviewer: "[name]"
  
  pre_interview:
    - Review account history (usage data, support tickets, NPS scores)
    - Check CRM for relationship context
    - Prepare 3 hypotheses to test
    
  warm_up: # 3-5 min
    - "Tell me about your role and what a typical week looks like."
    - "How long have you been using [product]?"
    - "[Acknowledge something specific about their usage]"
    
  context: # 5-10 min  
    - "What problem were you trying to solve when you found us?"
    - "What were you using before? What worked/didn't?"
    - "Walk me through how [product] fits into your workflow."
    
  core_exploration: # 15-20 min
    - "Walk me through the last time you used [specific feature]."
    - "What's the most valuable thing [product] does for you?"
    - "What's the most frustrating thing?"
    - "Tell me about a time [product] didn't work the way you expected."
    - "What workaround have you built because we're missing something?"
    
  outcome_assessment: # 5-10 min
    - "How do you measure the value you get from [product]?"
    - "What would happen if you lost access tomorrow?"
    - "On a scale of 1-10, how likely would you recommend us? Why that number?"
    
  future_vision: # 5 min
    - "If you had a magic wand, what would [product] do that it doesn't today?"
    - "What's changing in your world that we should know about?"
    
  close: # 2 min
    - "Anything I didn't ask that I should have?"
    - "Would you be open to joining our advisory group / beta testing?"
    - Thank + follow-up timeline
    
  post_interview:
    key_quotes: []
    surprises: []
    hypotheses_confirmed: []
    hypotheses_invalidated: []
    action_items: []
```

### Interview Techniques

**The Mom Test (Rob Fitzpatrick):**
- Talk about their life, not your idea
- Ask about specifics in the past, not hypotheticals
- Talk less, listen more
- Bad: "Would you use a feature that does X?" (they'll say yes to be nice)
- Good: "Tell me about the last time you tried to do X. What happened?"

**Five Whys for Root Cause:**
1. "That's frustrating. Why is that a problem for you?"
2. "Why does that matter to your work?"
3. "What happens when that goes wrong?"
4. "Why can't you work around it?"
5. "What would change if we fixed this?"

**Silence technique:** After they answer, count to 5 silently. They'll often add the most valuable insight in the silence.

**Mirror technique:** Repeat their last 3 words as a question. They'll elaborate without you leading.

### Interview Synthesis Template

After every 5 interviews in a batch:

```yaml
synthesis:
  batch: "[Interview batch name]"
  dates: "[range]"
  participants: "[count, segments]"
  
  themes:
    - theme: "[Name]"
      frequency: "[X of Y participants mentioned]"
      severity: "[Critical / High / Medium / Low]"
      representative_quotes:
        - "[exact quote]" — [participant type]
        - "[exact quote]" — [participant type]
      implications: "[what this means for product/business]"
      recommended_action: "[specific next step]"
      
  surprises:
    - "[Things you didn't expect]"
    
  segments_divergence:
    - "[Where different segments disagreed]"
    
  confidence_level: "[High / Medium / Low]"
  next_steps: []
```

---

## Phase 4: Feedback Taxonomy & Classification

### Category Hierarchy

```yaml
feedback_taxonomy:
  product:
    usability:
      - "Confusing UI / navigation"
      - "Feature hard to find"
      - "Too many steps to complete task"
      - "Mobile experience issues"
    functionality:
      - "Feature doesn't work as expected"
      - "Missing capability"
      - "Performance / speed"
      - "Integration issues"
    reliability:
      - "Bugs / errors"
      - "Data loss / corruption"
      - "Downtime / availability"
      
  experience:
    onboarding:
      - "Setup too complex"
      - "Documentation unclear"
      - "Time to value too long"
    support:
      - "Response time"
      - "Resolution quality"
      - "Self-service gaps"
    communication:
      - "Product updates unclear"
      - "Billing confusion"
      - "Status page / transparency"
      
  value:
    pricing:
      - "Too expensive"
      - "Wrong packaging / tiers"
      - "Hidden costs"
      - "Competitor cheaper"
    roi:
      - "Can't measure value"
      - "Not delivering promised results"
      - "Value decreased over time"
      
  strategic:
    market_fit:
      - "Wrong audience"
      - "Use case mismatch"
      - "Outgrew the product"
    competitive:
      - "Competitor has feature X"
      - "Switching to competitor"
      - "Industry trend we're missing"
```

### Sentiment Scoring

For every piece of feedback, score:

| Dimension | Scale | Guide |
|-----------|-------|-------|
| **Sentiment** | -2 to +2 | -2=angry, -1=frustrated, 0=neutral, +1=positive, +2=delighted |
| **Urgency** | 1-5 | 1=nice-to-have, 3=important, 5=blocking/churning |
| **Frequency** | Count | How many unique customers mention this |
| **Revenue at risk** | $ | ARR of customers mentioning this theme |
| **Effort to fix** | S/M/L/XL | Engineering estimate |

### Auto-Tagging Rules

When processing feedback, apply tags automatically:

```
IF contains("cancel", "churn", "leaving", "switching") → tag: churn_risk, urgency: 5
IF contains("bug", "error", "broken", "crash") → tag: bug_report, urgency: 4
IF contains("wish", "would be nice", "if only") → tag: feature_request, urgency: 2
IF contains("love", "amazing", "best") → tag: positive_signal, sentiment: +2
IF contains("competitor", "alternative", "other tool") → tag: competitive_intel
IF contains("price", "cost", "expensive", "cheaper") → tag: pricing_feedback
IF contains("confusing", "hard to", "can't figure") → tag: usability_issue, urgency: 3
```

---

## Phase 5: Metric Systems

### NPS (Net Promoter Score)

**Question:** "How likely are you to recommend [product] to a colleague? (0-10)"

**Scoring:**
- 0-6: Detractor
- 7-8: Passive
- 9-10: Promoter
- **NPS = % Promoters - % Detractors** (range: -100 to +100)

**Benchmarks by industry:**
| Industry | Poor | Average | Good | Excellent |
|----------|------|---------|------|-----------|
| SaaS B2B | <20 | 20-40 | 40-60 | 60+ |
| SaaS B2C | <10 | 10-30 | 30-50 | 50+ |
| E-commerce | <20 | 20-40 | 40-60 | 60+ |
| Financial Services | <10 | 10-30 | 30-50 | 50+ |
| Healthcare Tech | <15 | 15-35 | 35-55 | 55+ |

**NPS follow-up questions (by score):**
- Detractor (0-6): "We're sorry to hear that. What's the #1 thing we could improve?"
- Passive (7-8): "What would it take to make us a 9 or 10?"
- Promoter (9-10): "That's great! What do you value most about us?"

**NPS action rules:**
- Score dropped >10 points quarter-over-quarter → immediate investigation
- Detractor from Enterprise account → CSM alert within 24 hours
- Promoter → trigger referral/review/case study ask within 7 days

### CSAT (Customer Satisfaction Score)

**Question:** "How satisfied were you with [specific interaction]? (1-5)"
**Score:** (Satisfied responses [4-5] / Total responses) × 100

**Benchmarks:** 75% = decent, 85% = good, 90%+ = excellent

**When to use:** After specific interactions (support, onboarding, feature launch)

### CES (Customer Effort Score)

**Question:** "How easy was it to [specific task]? (1-7, 1=very difficult, 7=very easy)"
**Score:** Average of all responses

**Benchmarks:** <4 = high effort (problem), 4-5 = acceptable, 5+ = low effort (good)

**Why CES matters:** CES is the strongest predictor of future purchasing behavior. High-effort experiences drive 96% of disloyalty.

### Composite Health Score

Combine metrics for overall VoC health:

```yaml
voc_health_score:
  nps:
    weight: 30
    score: "[0-100 normalized: (NPS + 100) / 2]"
  csat:
    weight: 20
    score: "[CSAT %]"
  ces:
    weight: 15
    score: "[(CES / 7) × 100]"
  feedback_volume:
    weight: 10
    score: "[trend: increasing = good]"
  response_rate:
    weight: 10
    score: "[survey response rate %]"
  closed_loop_rate:
    weight: 15
    score: "[% of feedback items with documented response/action]"
    
  total: "[weighted sum / 100]"
  grade: "[A: 80+, B: 65-79, C: 50-64, D: 35-49, F: <35]"
```

---

## Phase 6: Feature Request Prioritization

### RICE + VoC Framework

Score each feature request:

| Factor | Formula | Weight |
|--------|---------|--------|
| **Reach** | # customers requesting (or affected) per quarter | 25% |
| **Impact** | Score 0.5 (minimal), 1 (low), 2 (medium), 3 (high) | 25% |
| **Confidence** | % confidence in estimates (50-100%) | 20% |
| **Effort** | Person-weeks to build | 15% |
| **Revenue Signal** | ARR at risk or expansion ARR | 15% |

**RICE-V Score = (Reach × Impact × Confidence × Revenue Signal) / Effort**

### Prioritization Decision Tree

```
1. Is this blocking revenue? (churn risk from top accounts)
   → YES: Fast-track (Sprint 1)
   → NO: Continue ↓

2. Does it affect >20% of customers?
   → YES: High priority (next quarter)
   → NO: Continue ↓

3. Is it from a strategic segment we're targeting?
   → YES: Medium-high priority
   → NO: Continue ↓

4. Does it align with product vision?
   → YES: Backlog with planned quarter
   → NO: Decline with explanation (close the loop!)
```

### Saying "No" Framework

Not every feature request should be built. Decline gracefully:

**Template:** "Thanks for this suggestion! We've heard this from [X] customers. Right now, our roadmap is focused on [theme] because [reason]. We're not planning to build this in the next [timeframe], but we've logged it. Here's what we ARE building that might help: [alternative]. We'll update this request if our plans change."

**When to say no:**
- Request serves <5% of customers
- Conflicts with product vision
- Better solved by integration/partner
- Effort/value ratio is poor
- Customer is better served by a different product

---

## Phase 7: Closed-Loop Workflow

### The Feedback Loop (4 stages)

```
COLLECT → ANALYZE → ACT → COMMUNICATE
    ↑                              |
    └──────────────────────────────┘
```

### Closed-Loop Response Templates

**Acknowledgment (within 24 hours):**
"Thanks for sharing this feedback. We've logged it as [category] and it's being reviewed by our [product/engineering] team. We'll update you when we have a plan."

**In Progress:**
"Quick update on your feedback about [topic] — we're actively working on this. Expected [timeframe]. Here's what's changing: [brief description]."

**Shipped:**
"Remember when you told us about [original feedback]? We fixed it! Here's what changed: [specific improvement]. Try it out and let us know what you think."

**Declined (see "Saying No" above)**

### Response SLAs by Feedback Type

| Type | Acknowledge | Triage | Resolve/Respond |
|------|------------|--------|-----------------|
| Bug report | 4 hours | 24 hours | Per severity SLA |
| Feature request | 48 hours | 1 week | Quarterly review |
| Complaint | 4 hours | 24 hours | 72 hours |
| Praise | 24 hours | N/A | Share internally |
| Churn feedback | 24 hours | 48 hours | 1 week (win-back) |
| NPS detractor | 24 hours | 48 hours | 1 week |

### Closed-Loop Tracking

```yaml
feedback_item:
  id: "FB-[YYYY]-[####]"
  source: "[channel]"
  customer: "[name, segment, ARR]"
  date_received: "[YYYY-MM-DD]"
  category: "[from taxonomy]"
  sentiment: "[-2 to +2]"
  urgency: "[1-5]"
  
  status: "[New | Acknowledged | Triaging | In Progress | Shipped | Declined | Won't Fix]"
  assigned_to: "[team/person]"
  
  date_acknowledged: "[YYYY-MM-DD]"
  date_resolved: "[YYYY-MM-DD]"
  resolution: "[what was done]"
  customer_notified: "[yes/no + date]"
  customer_satisfied: "[yes/no/unknown]"
  
  linked_items:
    jira: "[ticket ID]"
    roadmap: "[feature/initiative]"
    other_feedback: "[related FB IDs]"
```

---

## Phase 8: VoC Reporting & Dashboards

### Weekly VoC Summary

```yaml
weekly_voc:
  period: "[week of YYYY-MM-DD]"
  
  volume:
    total_feedback: "[count]"
    by_channel:
      support: "[count]"
      in_app: "[count]"
      surveys: "[count]"
      interviews: "[count]"
    trend: "[↑/↓/→ vs last week]"
    
  metrics:
    nps: "[score] ([↑/↓] [X] from last period)"
    csat: "[%] ([↑/↓] [X]%)"
    ces: "[score] ([↑/↓])"
    
  top_themes:
    - theme: "[#1 theme]"
      mentions: "[count]"
      sentiment: "[avg]"
      revenue_at_risk: "[$]"
      action: "[what we're doing]"
    - theme: "[#2]"
      # ...
    - theme: "[#3]"
      # ...
      
  alerts:
    - "[Enterprise detractor: Company X, NPS dropped from 8 to 3]"
    - "[New theme emerging: Y mentioned by 5 customers this week]"
    
  closed_loop:
    items_received: "[count]"
    items_acknowledged: "[count] ([%])"
    items_resolved: "[count]"
    avg_resolution_time: "[days]"
    
  wins:
    - "[Positive feedback / testimonial / case study lead]"
```

### Monthly VoC Report (for leadership)

**Structure:**
1. **Executive summary** — 3 bullet headline (NPS trend, top risk, top opportunity)
2. **Metric trends** — NPS/CSAT/CES with month-over-month and quarter-over-quarter
3. **Theme analysis** — Top 5 themes with frequency, sentiment, revenue impact
4. **Segment breakdown** — Feedback patterns by customer segment
5. **Competitive signals** — What customers say about competitors
6. **Roadmap alignment** — How feedback maps to current roadmap
7. **Action items** — What we're doing about top themes
8. **Closed-loop performance** — % acknowledged, % resolved, avg time

### Quarterly Strategic VoC Review

Go deeper quarterly:
- **Cohort analysis:** Do newer customers have different feedback patterns?
- **Segment analysis:** Which segments are happiest/unhappiest?
- **Journey mapping:** Where in the journey does feedback spike?
- **Trend analysis:** Which themes are growing/shrinking?
- **Competitive landscape:** Are we gaining or losing on key dimensions?
- **ROI of changes:** Did features we shipped based on feedback improve metrics?

---

## Phase 9: VoC-Driven Product Decisions

### Evidence Hierarchy

When making product decisions, rank evidence:

1. **Behavioral data** (what they DO) — usage analytics, conversion, retention
2. **Revealed preferences** (what they PAY for) — upgrade triggers, pricing experiments
3. **Qualitative interviews** (what they SAY in depth) — discovery, satisfaction
4. **Survey data** (what they REPORT) — NPS, CSAT, feature votes
5. **Support tickets** (what they COMPLAIN about) — pain points
6. **Feature request votes** (what they ASK for) — stated preferences
7. **Social/review feedback** (what they TELL others) — public sentiment

**Rule:** Never build based on Level 6-7 alone. Always triangulate with Level 1-3.

### Product Decision Template

```yaml
product_decision:
  what: "[Feature/change being considered]"
  
  voc_evidence:
    quantitative:
      customers_requesting: "[count]"
      arr_represented: "[$]"
      nps_impact: "[detractors mentioning this]"
      support_tickets: "[count related]"
    qualitative:
      interview_quotes:
        - "[quote]" — [segment]
      themes_connected: "[from taxonomy]"
    behavioral:
      usage_data: "[relevant metrics]"
      churn_correlation: "[if applicable]"
      
  decision: "[Build / Decline / Investigate further]"
  confidence: "[High / Medium / Low]"
  expected_impact:
    nps_change: "[estimated]"
    churn_reduction: "[estimated]"
    expansion_revenue: "[estimated]"
    
  success_metrics:
    - "[How we'll know this worked]"
  review_date: "[When to check impact]"
```

---

## Phase 10: Advanced VoC Patterns

### Customer Advisory Board (CAB)

**Structure:**
- 8-12 customers across segments
- Quarterly 90-minute sessions
- Mix: 60% product roadmap feedback, 20% industry trends, 20% relationship building
- Incentive: Early access to features, executive access, influence on roadmap

**Selection criteria:**
- Represents target segment
- Engaged user (not just big logo)
- Constructive (not just complainers or cheerleaders)
- Diverse use cases
- Willing to commit time

### Competitive Feedback Mining

When customers mention competitors:

```yaml
competitive_mention:
  competitor: "[name]"
  context: "[switching to / comparing / switched from]"
  feature_gap: "[what competitor has that we don't]"
  our_advantage: "[what they like about us vs competitor]"
  customer_segment: "[type]"
  deal_size: "[$]"
  action: "[product response needed?]"
```

Track quarterly: "Competitor mention frequency" — rising mentions of a specific competitor = early warning.

### Feedback-Driven Pricing Insights

Customer feedback reveals pricing issues:

| Signal | Meaning | Action |
|--------|---------|--------|
| "Too expensive" with no specifics | Perception problem, not price problem | Improve value communication |
| "Feature X should be in my plan" | Packaging issue | Review tier boundaries |
| "Competitor is cheaper" | Price positioning | Competitive analysis |
| "I'd pay more for Y" | Expansion opportunity | Test premium tier/add-on |
| "Not sure what I'm paying for" | Value clarity gap | Improve billing page, add ROI dashboard |

### Multi-Product VoC

If you have multiple products:
- Separate NPS per product (not one company NPS)
- Cross-product feedback: "I wish [Product A] did what [Product B] does"
- Unified customer view: all feedback across products in one place
- Cross-sell signals in feedback: mentions of adjacent problems

### VoC for Pre-PMF Companies

Simplified system when you have <50 customers:

1. **Talk to every customer** — monthly calls, 20 minutes
2. **Track in a spreadsheet** — name, date, feedback, theme, action taken
3. **One metric:** Sean Ellis test — "How would you feel if you could no longer use [product]?" (>40% "very disappointed" = PMF)
4. **Ship weekly, ask weekly** — tight feedback loop
5. **Don't survey** — sample size too small, just talk

---

## Phase 11: Edge Cases

### Negative Feedback Spike
- **Don't panic.** Check: is it a bug (concentrated), a change (adoption curve), or a trend (systemic)?
- **Triage:** Is it one loud customer or multiple independent voices?
- **Respond:** Acknowledge publicly if visible (social, reviews). Fix if bug. Explain if change.

### Feedback Contradictions
- Segment A wants simplicity, Segment B wants power features
- **Resolution:** Check which segment is your ICP. Build for ICP, offer workarounds for others. Consider tiered product.

### Survey Fatigue
- Response rates dropping below 10% = fatigue
- **Fix:** Reduce frequency, make surveys shorter, show impact ("You told us X, we built Y"), vary channels

### Vocal Minority Problem
- 3 customers scream for feature X, 300 silently use feature Y
- **Rule:** Never prioritize by volume of complaints alone. Cross-reference with usage data and revenue.

### Cultural Differences (International)
- NPS scores vary by culture (Japan averages lower, US averages higher)
- **Fix:** Benchmark within regions, not globally. Adjust expectations by market.

### Feedback from Free Users
- Lower weight than paying customers for prioritization
- BUT valuable for: conversion barriers, first-impression issues, market understanding
- **Rule:** Track separately. Flag "conversion blockers" for growth team.

---

## Quality Scoring Rubric

Rate your VoC program (0-100):

| Dimension | Weight | 0-25 | 50 | 75 | 100 |
|-----------|--------|------|----|----|-----|
| **Collection coverage** | 15% | 1 channel | 3 channels | 5+ channels | Full journey coverage |
| **Analysis depth** | 15% | Read comments | Categorize | Quantified themes | Predictive insights |
| **Response time** | 10% | Weeks | Days | Hours | Real-time SLA met |
| **Closed-loop rate** | 15% | <20% | 40-60% | 60-80% | >80% with satisfaction check |
| **Decision influence** | 15% | Ignored | Occasional input | Regular roadmap input | Systematic decision driver |
| **Metric tracking** | 10% | None | NPS exists | NPS + CSAT + CES | Full suite + benchmarks |
| **Segmentation** | 10% | None | By plan tier | Multi-dimensional | Persona-level insights |
| **ROI measurement** | 10% | None | Anecdotal | Feature-level impact | Revenue-attributed |

---

## Natural Language Commands

Use these to interact:

1. **"Set up VoC program"** → Generate program brief + collection channels + first survey
2. **"Design NPS survey"** → Create NPS survey with follow-ups + distribution plan
3. **"Prep customer interview"** → Generate interview guide for specific customer/type
4. **"Analyze this feedback"** → Categorize, score sentiment, tag, recommend action
5. **"Synthesize interview batch"** → Create synthesis from multiple interview notes
6. **"Prioritize feature requests"** → RICE-V score + prioritization recommendation
7. **"Generate VoC report"** → Weekly/monthly/quarterly report from data
8. **"Score our VoC program"** → Run maturity assessment + improvement recommendations
9. **"Close the loop on [item]"** → Generate appropriate response for feedback item
10. **"Compare our NPS to benchmarks"** → Industry benchmark comparison + trend analysis
11. **"Find churn signals in feedback"** → Analyze feedback for churn risk patterns
12. **"Build customer advisory board"** → Selection criteria + program structure + first agenda

---

*Built by AfrexAI — Turning customer voices into revenue decisions.*
