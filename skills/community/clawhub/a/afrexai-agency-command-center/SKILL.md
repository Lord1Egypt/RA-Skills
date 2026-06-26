---
name: Agency Command Center
slug: afrexai-agency-command-center
version: 1.0.0
description: Complete agency operations system — client lifecycle, pricing, project delivery, team management, and growth strategy for service businesses.
tags: agency, consulting, client management, project management, freelance, professional services
---

# Agency Command Center

Complete operations system for service agencies, consultancies, and freelance businesses. From first client inquiry to recurring revenue machine.

## When to Use

- Starting or scaling a service business (dev, marketing, design, consulting, AI/automation)
- Managing multiple clients and projects simultaneously
- Building repeatable processes for client delivery
- Pricing services and writing proposals
- Growing from solo to team

---

## Phase 1: Agency Foundation

### Business Model Selection

Choose your model — this drives everything else:

| Model | Typical ACV | Team Size | Margin Target | Best For |
|-------|------------|-----------|---------------|----------|
| Solo Expert | $5K-$25K | 1 | 60-80% | Deep specialists |
| Boutique | $25K-$100K | 3-8 | 40-55% | Quality-focused niche |
| Growth Agency | $100K-$500K | 10-30 | 30-45% | Scale players |
| Productized Service | $1K-$10K/mo | 5-15 | 50-70% | Repeatable delivery |

### Service Packaging Framework

**Don't sell time. Sell outcomes.**

Structure services into 3 tiers:

```yaml
service_catalog:
  tier_1_starter:
    name: "[Quick Win Name]"
    price: "$X,XXX"
    duration: "1-2 weeks"
    deliverables:
      - "[Specific deliverable 1]"
      - "[Specific deliverable 2]"
    ideal_for: "Companies that need [specific outcome] fast"
    margin_target: "70%+"
    
  tier_2_standard:
    name: "[Core Service Name]"
    price: "$XX,XXX"
    duration: "4-8 weeks"
    deliverables:
      - "[Everything in Tier 1]"
      - "[Additional deliverable 3]"
      - "[Additional deliverable 4]"
    ideal_for: "Companies ready for [bigger transformation]"
    margin_target: "50%+"
    
  tier_3_premium:
    name: "[Flagship Engagement Name]"
    price: "$XXX,XXX+"
    duration: "3-6 months"
    deliverables:
      - "[Everything in Tier 2]"
      - "[Strategic deliverable 5]"
      - "[Ongoing support/retainer]"
    ideal_for: "Enterprises needing [complete solution]"
    margin_target: "40%+"
```

### Niche Selection Scorecard

Rate each potential niche 1-5:

| Criterion | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Market size (enough clients?) | 3x | /5 | /15 |
| Willingness to pay ($10K+ deals?) | 3x | /5 | /15 |
| Your expertise (can you deliver?) | 2x | /5 | /10 |
| Competition (room for you?) | 2x | /5 | /10 |
| Passion (can you do this for years?) | 1x | /5 | /5 |
| **Total** | | | **/55** |

**35+ = strong niche.** Below 25 = keep looking.

---

## Phase 2: Client Acquisition Engine

### Inbound Lead Qualification (BANT-S)

When an inquiry arrives, extract:

```yaml
lead_qualification:
  company: ""
  contact_name: ""
  contact_role: ""
  source: ""  # referral, website, social, cold
  
  budget:
    stated: ""
    estimated_range: ""
    budget_holder: ""  # Are they the decision maker?
    
  authority:
    decision_maker: true/false
    other_stakeholders: []
    approval_process: ""
    
  need:
    problem_statement: ""
    urgency: "low|medium|high|critical"
    current_solution: ""
    why_change_now: ""
    
  timeline:
    desired_start: ""
    desired_completion: ""
    hard_deadlines: []
    
  scope_fit:
    matches_services: true/false
    complexity: "simple|moderate|complex|enterprise"
    red_flags: []

  score: "/100"  # See scoring below
```

### Lead Scoring (0-100)

| Factor | Points | Criteria |
|--------|--------|----------|
| Budget match | 0-25 | 25=confirmed budget in range, 15=likely, 5=unclear, 0=way below |
| Authority | 0-20 | 20=decision maker, 10=influencer, 0=researcher |
| Need urgency | 0-20 | 20=critical/deadline, 15=high, 10=medium, 5=exploring |
| Timeline fit | 0-15 | 15=aligns with capacity, 10=tight but doable, 0=impossible |
| Scope fit | 0-10 | 10=core service, 5=adjacent, 0=outside expertise |
| Source quality | 0-10 | 10=referral, 7=inbound, 3=cold |

**80+ = fast track** (respond within 2 hours)
**60-79 = standard** (respond within 24 hours)
**40-59 = nurture** (add to drip, check back in 30 days)
**Below 40 = decline gracefully**

### Discovery Call Framework (45 min)

```
[0-5 min] Rapport + Agenda Setting
- "Thanks for taking the time. Here's what I'd like to cover..."
- Confirm their role and who else is involved in the decision

[5-20 min] Deep Problem Discovery
- "Walk me through what's happening today..."
- "What have you tried so far?"
- "What's the cost of NOT solving this?" ← KEY QUESTION
- "If we solve this perfectly, what does that look like in 6 months?"
- "What's your biggest concern about working with an agency?"

[20-30 min] Solution Exploration
- Mirror their language back: "So the core issue is [X], and ideally you'd have [Y]"
- Share relevant case study (1-2 min, not a pitch)
- Outline potential approach at high level
- "Based on what you've described, I'd suggest [Tier 2 service]"

[30-40 min] Logistics
- Timeline expectations
- Budget conversation: "Projects like this typically range $X-$Y. Does that align with what you had in mind?"
- Decision process and stakeholders
- Required access/resources from their side

[40-45 min] Next Steps
- "Here's exactly what happens next: I'll send a proposal by [date]..."
- Confirm follow-up date
- Ask: "Is there anything else I should know before putting this together?"
```

### Outreach Templates

**Warm Referral Follow-up:**
```
Subject: [Referrer] suggested we connect

Hi [Name],

[Referrer] mentioned you're dealing with [specific problem]. We just helped [similar company] solve that — they went from [before state] to [after state] in [timeframe].

Worth a 20-minute call to see if we can do the same for you?

[Your name]
```

**Post-Discovery Proposal Email:**
```
Subject: Your [problem] solution — proposal attached

Hi [Name],

Great talking on [day]. Attached is the proposal for [project name].

The quick version:
- We'll deliver [key outcome] by [date]
- Investment: $[amount]
- You'll see [specific metric improvement]

I've blocked [date] for a 15-min walkthrough if that works.

[Your name]
```

---

## Phase 3: Proposal & Pricing Engine

### Proposal Structure (Win Rate Optimizer)

Every proposal follows this structure:

```
1. EXECUTIVE SUMMARY (1 page)
   - Their problem in their words (mirror discovery call)
   - The cost of inaction (quantified)
   - Your recommended solution (1 paragraph)
   - Investment and timeline (bottom line up front)

2. SITUATION ANALYSIS (1-2 pages)
   - Current state (show you listened)
   - Desired future state
   - Gap analysis
   - Why now matters

3. RECOMMENDED APPROACH (2-3 pages)
   - Phase breakdown with deliverables
   - Timeline with milestones
   - What success looks like (measurable)
   - Your methodology/framework name

4. INVESTMENT (1 page)
   - 3-tier pricing (Good/Better/Best)
   - What's included in each tier
   - Payment terms
   - What's NOT included (scope boundaries)

5. WHY US (1 page)
   - 2-3 relevant case studies (results, not process)
   - Team bios (relevant experience only)
   - Unique approach/methodology

6. NEXT STEPS (half page)
   - Clear call to action
   - Timeline to start
   - What you need from them
```

### Pricing Calculator

```yaml
pricing_worksheet:
  # Cost basis
  estimated_hours: 0
  blended_hourly_rate: 0  # Your internal cost per hour
  direct_costs: 0  # Software, contractors, etc.
  total_cost: 0  # hours × rate + direct costs
  
  # Value basis
  client_problem_cost: 0  # Annual cost of their problem
  your_solution_value: 0  # Annual value you create
  value_price: 0  # 10-20% of value created
  
  # Market basis
  competitor_low: 0
  competitor_high: 0
  market_price: 0  # Your positioning in range
  
  # Final price
  floor_price: 0  # cost × 1.5 (minimum viable margin)
  target_price: 0  # MAX(value_price, market_price)
  anchor_price: 0  # target × 1.3 (your Tier 3)
  
  # Sanity checks
  margin_percent: 0  # Must be > 40%
  price_per_hour_effective: 0  # Must be > 2× your cost rate
  roi_for_client: "X:1"  # Must be > 3:1 or rethink
```

### Pricing Rules

1. **Never price by the hour externally** — always project or value-based
2. **Always present 3 options** — anchors the middle option as "reasonable"
3. **Include a "quick start" option** — low-risk entry point ($2K-$5K)
4. **50% upfront, 50% on completion** for projects under $25K
5. **Monthly retainers: 3-month minimum** — shorter isn't worth onboarding cost
6. **Scope creep clause**: "Additional requests beyond this scope will be quoted separately"
7. **Price increases**: raise prices 10-15% annually, grandfather existing clients for 6 months

### Retainer Model Design

```yaml
retainer_tiers:
  growth:
    monthly_fee: "$X,XXX"
    hours_included: 20
    response_time: "24 hours"
    includes:
      - "[Core service deliverable]"
      - "Monthly strategy call"
      - "Slack/email support"
    overage_rate: "$XXX/hr"
    
  scale:
    monthly_fee: "$XX,XXX"
    hours_included: 40
    response_time: "4 hours"
    includes:
      - "[Everything in Growth]"
      - "[Additional strategic service]"
      - "Weekly check-in call"
      - "Quarterly business review"
    overage_rate: "$XXX/hr"
    
  enterprise:
    monthly_fee: "$XX,XXX+"
    hours_included: "Unlimited (fair use)"
    response_time: "2 hours"
    includes:
      - "[Everything in Scale]"
      - "Dedicated team member"
      - "24/7 emergency support"
      - "Executive sponsor access"
    overage_rate: "N/A"
```

---

## Phase 4: Client Onboarding System

### Onboarding Checklist (First 48 Hours)

```yaml
onboarding:
  day_0_signed:
    - [ ] Contract signed and countersigned
    - [ ] First payment received
    - [ ] Welcome email sent (see template below)
    - [ ] Client folder created in project management
    - [ ] Internal kickoff scheduled
    - [ ] Client added to communication channel
    
  day_1:
    - [ ] Access credentials collected (see access request template)
    - [ ] Onboarding questionnaire sent
    - [ ] Project timeline shared
    - [ ] Team introductions made
    - [ ] First milestone confirmed
    
  day_2:
    - [ ] Kickoff call completed
    - [ ] Meeting notes distributed
    - [ ] First deliverable timeline confirmed
    - [ ] Weekly check-in cadence set
    - [ ] Client expectations document signed
```

### Welcome Email Template

```
Subject: Welcome to [Agency Name] — here's what happens next

Hi [Name],

We're excited to get started on [project name]. Here's your roadmap for the next 48 hours:

TODAY:
✅ Contract signed — check
✅ You'll receive an onboarding questionnaire (10 min to complete)
✅ We'll send access requests for [systems we need]

TOMORROW:
📋 We review your questionnaire answers
📞 Kickoff call at [time] — here's the agenda: [link]

THIS WEEK:
🚀 First milestone: [deliverable] by [date]
📊 Weekly update every [day] at [time]

YOUR TEAM:
- [Name] — Project Lead (your main point of contact)
- [Name] — [Role]
- For urgent issues: [emergency contact method]

Questions before kickoff? Reply to this email or message us on [Slack/channel].

Let's build something great.

[Your name]
```

### Client Expectations Document

Get this signed at onboarding to prevent 90% of problems:

```
WORKING AGREEMENT

Communication:
- Primary channel: [Slack/email/tool]
- Response time: We respond within [X hours] on business days
- Urgent issues: [Phone/emergency process]
- Weekly updates: Every [day] by [time]

Feedback & Approvals:
- We'll send work for review with clear deadlines
- Feedback is due within [48 hours] of submission
- Delayed feedback = delayed timeline (no penalty to us)
- "Approved" means approved — revisions after approval are billed separately

Scope:
- This project covers: [specific deliverables from contract]
- Changes to scope require a written change order
- We'll flag scope creep early — no surprise invoices

Meetings:
- Weekly check-in: [30 min, day/time]
- We'll send agendas 24h before, notes within 24h after
- Cancel with 24h notice or it counts as held
```

---

## Phase 5: Project Delivery System

### Project Tracking Template

```yaml
project:
  name: ""
  client: ""
  status: "active|on-hold|at-risk|complete"
  
  health:
    schedule: "green|yellow|red"
    budget: "green|yellow|red"
    scope: "green|yellow|red"
    client_satisfaction: "green|yellow|red"
    overall: "green|yellow|red"
  
  financials:
    contract_value: 0
    collected: 0
    outstanding: 0
    hours_budgeted: 0
    hours_used: 0
    burn_rate_percent: 0  # hours_used / hours_budgeted × 100
    margin_actual: 0
    
  milestones:
    - name: ""
      due: "YYYY-MM-DD"
      status: "pending|in-progress|review|complete|late"
      deliverables: []
      
  risks:
    - description: ""
      probability: "low|medium|high"
      impact: "low|medium|high"
      mitigation: ""
      
  next_actions:
    - task: ""
      owner: ""
      due: "YYYY-MM-DD"
```

### Weekly Client Update Template

Send every week, same day, same time:

```
Subject: [Project Name] — Weekly Update #[N]

📊 STATUS: [GREEN/YELLOW/RED]

COMPLETED THIS WEEK:
✅ [Deliverable/milestone 1]
✅ [Deliverable/milestone 2]

IN PROGRESS:
🔄 [Task 1] — [% complete, expected done date]
🔄 [Task 2] — [% complete, expected done date]

NEXT WEEK:
📋 [Planned deliverable 1]
📋 [Planned deliverable 2]

⚠️ NEEDS YOUR INPUT:
- [Decision/approval/access needed] — please respond by [date]

TIMELINE: [On track / X days ahead / X days behind]
BUDGET: [X% used of total hours]
```

### Scope Creep Management

When a client requests something outside scope:

**Step 1: Acknowledge** — "Great idea — let me look at what that involves."

**Step 2: Classify:**
- **Tiny** (<2 hours, improves deliverable) → Do it, note it as goodwill
- **Small** (2-8 hours) → "Happy to add this. It's about [X hours] additional work, so roughly $[amount]. Want me to write up a quick change order?"
- **Large** (8+ hours) → "This is actually a separate project. Let me scope it properly and send you an estimate."

**Step 3: Document** — Every change request logged:
```yaml
change_request:
  date: ""
  requested_by: ""
  description: ""
  classification: "goodwill|change_order|new_project"
  estimated_hours: 0
  estimated_cost: 0
  status: "pending|approved|declined"
  impact_on_timeline: ""
```

### Quality Control Checklist

Before ANY deliverable goes to client:

- [ ] Meets brief requirements (check against original scope)
- [ ] Reviewed by someone other than the creator
- [ ] Tested/proofread (no broken links, typos, errors)
- [ ] Formatted professionally (consistent branding)
- [ ] Includes context ("Here's the [deliverable]. Key decisions we made: [X, Y, Z]")
- [ ] Clear next steps stated
- [ ] Sent with enough time for client to review before deadline

---

## Phase 6: Team & Operations

### Hiring Decision Framework

**When to hire vs. contract:**

| Factor | Hire Full-Time | Contract/Freelance |
|--------|---------------|-------------------|
| Need frequency | Ongoing, daily | Project-based, sporadic |
| Skill specificity | Core to your service | Specialized/niche |
| Client interaction | Client-facing | Behind the scenes |
| Cost at current volume | Cheaper than contracting | Cheaper than hiring |
| Ramp-up time | Worth the investment | Need them productive Day 1 |

### Team Utilization Tracking

```yaml
team_member:
  name: ""
  role: ""
  cost_per_hour: 0  # Your cost (salary ÷ working hours)
  billable_target: "70%"  # % of time on client work
  
  this_week:
    total_hours: 40
    billable_hours: 0
    internal_hours: 0  # Sales, admin, training
    utilization: "0%"
    
  this_month:
    billable_hours: 0
    revenue_generated: 0
    effective_rate: 0  # revenue ÷ billable hours
```

**Utilization targets:**
- **Below 60%** = underutilized (need more clients or reduce headcount)
- **60-75%** = healthy (room for training, sales, admin)
- **75-85%** = optimal (high output, sustainable)
- **Above 85%** = burnout risk (hire or stop taking new work)

### Delegation Framework

As agency grows, delegate in this order:

1. **Execution** (first hire) — Someone to do the work you've been doing
2. **Project Management** — Someone to manage timelines and client comms
3. **Sales** — Someone to handle inbound and proposals
4. **Operations** — Someone to handle invoicing, onboarding, admin
5. **Strategy** — Only delegate last (this is your competitive advantage)

### Standard Operating Procedures (SOP) Template

Create one SOP per repeated process:

```yaml
sop:
  name: ""
  owner: ""
  last_updated: ""
  frequency: ""  # How often this runs
  
  purpose: ""  # Why this exists
  
  trigger: ""  # What kicks this off
  
  steps:
    - step: 1
      action: ""
      tool: ""  # What software/tool
      time: ""  # Expected duration
      output: ""  # What this step produces
      notes: ""
      
  quality_check: ""  # How to verify it's done right
  
  common_mistakes:
    - mistake: ""
      prevention: ""
```

---

## Phase 7: Financial Management

### Monthly P&L Dashboard

Track monthly, review weekly:

```yaml
monthly_financials:
  month: "YYYY-MM"
  
  revenue:
    project_revenue: 0
    retainer_revenue: 0
    other_revenue: 0
    total_revenue: 0
    
  cost_of_delivery:
    team_costs: 0  # Salaries/contractor payments for delivery
    software_tools: 0
    direct_expenses: 0  # Client-specific costs
    total_cod: 0
    
  gross_margin: 0  # revenue - cost_of_delivery
  gross_margin_percent: 0  # Should be > 50%
  
  operating_expenses:
    sales_marketing: 0
    admin_overhead: 0
    office_insurance: 0
    total_opex: 0
    
  net_profit: 0  # gross_margin - opex
  net_margin_percent: 0  # Target: 15-25%
  
  cash:
    opening_balance: 0
    cash_in: 0  # Actually received
    cash_out: 0  # Actually paid
    closing_balance: 0
    runway_months: 0  # closing ÷ monthly burn
    
  ar_aging:
    current: 0  # Not yet due
    days_30: 0
    days_60: 0
    days_90_plus: 0  # Chase these aggressively
```

### Cash Flow Rules

1. **3-month cash reserve minimum** — always
2. **Invoice immediately** upon milestone completion — never wait
3. **Net 14 terms** for small clients, Net 30 for enterprise
4. **Chase at Day 7** past due (friendly), Day 14 (firm), Day 21 (final notice)
5. **Stop work at 30 days overdue** — no exceptions
6. **Retainer clients pay in advance** — not arrears

### Late Payment Sequence

```
Day 1 past due — Automated reminder:
"Hi [Name], friendly reminder that invoice #[X] for $[amount] was due on [date]. 
Payment link: [link]. Let me know if you have any questions."

Day 7 — Personal follow-up:
"Hi [Name], following up on invoice #[X]. Is everything okay? 
Happy to jump on a quick call if there's an issue with the invoice."

Day 14 — Firm notice:
"Hi [Name], invoice #[X] is now 14 days overdue. Per our agreement, 
work will pause on [date] if payment isn't received. 
Please process this at your earliest convenience."

Day 21 — Final notice:
"Hi [Name], this is a final notice for invoice #[X] ($[amount], 21 days overdue). 
Work on [project] will pause effective [date + 3 days] until payment is received. 
If there's a cash flow issue, let's discuss a payment plan."

Day 30 — Work stops. Send formal letter. Consider collections for large amounts.
```

---

## Phase 8: Client Retention & Growth

### Client Health Score (0-100)

Monitor monthly for each client:

| Dimension | Weight | Indicators | Score |
|-----------|--------|-----------|-------|
| Engagement | 25% | Response time, meeting attendance, feedback quality | /25 |
| Satisfaction | 25% | Explicit feedback, NPS, complaint frequency | /25 |
| Financial | 20% | Pays on time, budget discussions, upsell receptivity | /20 |
| Results | 20% | KPIs trending up, milestones hit, ROI demonstrated | /20 |
| Relationship | 10% | Champion strength, stakeholder breadth, referral likelihood | /10 |

**80+ = Healthy** — maintain and grow
**60-79 = Watch** — proactive check-in needed
**Below 60 = At risk** — intervention required

### Expansion Revenue Playbook

**Signals a client is ready to buy more:**
- Asking about services you haven't pitched
- Referring you to colleagues
- Saying "Can you also...?"
- Achieving ROI on current engagement
- New initiative/budget cycle starting
- Key stakeholder promoted (bigger budget)

**Upsell conversation opener:**
"We've delivered [result] on [project]. Based on what I'm seeing, there's an opportunity to [specific next outcome]. Want me to put together a quick proposal?"

### Quarterly Business Review (QBR) Template

For retainer clients, do this every 90 days:

```
1. RESULTS RECAP (10 min)
   - KPIs: where we started vs. where we are
   - Key wins this quarter
   - ROI calculation

2. WHAT WORKED / WHAT DIDN'T (10 min)
   - Honest assessment of delivery
   - Process improvements made
   - Client feedback addressed

3. MARKET/INDUSTRY CONTEXT (5 min)
   - Relevant trends affecting their business
   - What competitors are doing
   - New opportunities you've spotted

4. NEXT QUARTER PLAN (10 min)
   - Recommended priorities
   - New ideas/initiatives to explore
   - Resource/budget implications

5. RELATIONSHIP CHECK (5 min)
   - "How's our communication working?"
   - "Anything we should do differently?"
   - "Anyone else on your team we should loop in?"
```

### Client Offboarding (When They Leave)

Handle gracefully — they might come back or refer others:

```yaml
offboarding:
  - [ ] Exit interview (what went well, what didn't)
  - [ ] Final deliverables transferred
  - [ ] All access/credentials returned
  - [ ] Final invoice sent and collected
  - [ ] Knowledge transfer document provided
  - [ ] Testimonial requested (if relationship was positive)
  - [ ] Added to alumni newsletter/updates list
  - [ ] CRM status updated with reason for churn
  - [ ] Internal retrospective completed
  - [ ] Set 90-day re-engagement reminder
```

---

## Phase 9: Agency Growth Strategy

### Revenue Concentration Risk

**Rule: No single client > 30% of revenue.**

If one client dominates:
- Actively prospect new clients to dilute
- Don't hire specifically for that client
- Build savings buffer equal to their monthly revenue
- Diversify contact points (don't rely on one champion)

### Growth Levers (In Priority Order)

1. **Raise prices** — 10% increase = ~25% profit increase. Do this annually.
2. **Increase scope with existing clients** — cheapest growth. Upsell, cross-sell.
3. **Get referrals** — ask happy clients. "Who else do you know dealing with [problem]?"
4. **Improve close rate** — better proposals, faster follow-up, case studies.
5. **Generate more leads** — content, partnerships, paid ads (most expensive, do last).

### Productized Service Ladder

The path from custom services to scalable revenue:

```
Stage 1: Custom Projects (high margin, low scale)
↓ Identify repeated patterns
Stage 2: Templated Delivery (faster, more consistent)
↓ Package into fixed-scope offers
Stage 3: Productized Service (fixed price, predictable delivery)
↓ Build self-serve tools
Stage 4: Product + Service Hybrid (highest scale)
```

### Agency Metrics Dashboard

Track weekly:

```yaml
agency_dashboard:
  week_of: "YYYY-MM-DD"
  
  pipeline:
    new_leads: 0
    proposals_sent: 0
    proposals_won: 0
    win_rate: "0%"
    average_deal_size: 0
    pipeline_value: 0
    
  delivery:
    active_projects: 0
    projects_on_track: 0
    projects_at_risk: 0
    milestones_hit: 0
    milestones_missed: 0
    client_nps: 0
    
  financial:
    mrr: 0  # Monthly recurring revenue
    project_revenue: 0
    total_revenue: 0
    ar_outstanding: 0
    cash_position: 0
    
  team:
    avg_utilization: "0%"
    team_size: 0
    open_positions: 0
    attrition_ytd: 0
    
  growth:
    revenue_vs_last_month: "+0%"
    revenue_vs_last_year: "+0%"
    client_count: 0
    net_revenue_retention: "0%"  # Target: >110%
```

---

## Phase 10: Edge Cases & Advanced

### Difficult Client Playbooks

**The Scope Creeper:**
- Set hard boundaries in writing at kickoff
- Every request gets classified (see Phase 5)
- Track cumulative "free" work — present data quarterly
- If chronic: "We've absorbed $X in extra scope. Going forward, all additions go through change orders."

**The Ghost:**
- Missing reviews block YOUR team — lost productivity
- After 48h silence: "Just checking in — we need your feedback on [X] to stay on schedule."
- After 72h: "Heads up — without feedback by [date], the milestone will shift by [days]."
- Build into contract: "Client delays extend timeline 1:1"

**The Everything-Is-Urgent:**
- Define urgent vs. important at onboarding
- "We can prioritize this, but it means [other thing] moves to next week. Which matters more?"
- If chronic: introduce an "expedite fee" (25-50% premium for rush work)

**The Micromanager:**
- Over-communicate proactively — they micromanage because they're anxious
- Daily updates instead of weekly
- Share your process: "Here's exactly how we'll approach this and when you'll see progress"
- Give them a "status dashboard" they can check anytime

### Multi-Project Capacity Planning

```yaml
capacity:
  total_team_hours_weekly: 0
  billable_target_hours: 0  # total × 0.75
  currently_committed: 0
  available_hours: 0
  
  projects:
    - name: ""
      hours_per_week: 0
      weeks_remaining: 0
      team_members: []
      
  can_take_new_work: true/false  # available > 20 hours
  next_availability: "YYYY-MM-DD"
```

### Subcontractor Management

When outsourcing parts of delivery:

- **Never let the client communicate directly with subs** — you're the brand
- **Mark up subcontractor rates 30-50%** — you provide the client, the brief, and the QC
- **Pay subs within 7 days** of their invoice — builds loyalty
- **NDA + non-compete** — prevent them poaching your clients
- **Quality check everything** before it touches the client

### Remote/Async Operations

- **Default to async** — meetings are expensive (multiple people × time × context switch)
- **Document everything** — if it's not written, it didn't happen
- **Time zone rules**: overlap minimum 3 hours with client; respond during THEIR business hours
- **Weekly sync is sacred** — this is the one meeting that cannot be async
- **SOPs for everything** — the person doing the work shouldn't need to ask how

---

## Natural Language Commands

| Say | Agent Does |
|-----|-----------|
| "New lead from [company]" | Create lead qualification with BANT-S scoring |
| "Write proposal for [project]" | Generate proposal using framework |
| "Price this: [scope description]" | Run pricing calculator with 3-tier output |
| "Onboard [client name]" | Generate onboarding checklist and welcome email |
| "Weekly update for [client]" | Generate status update from project data |
| "Client health check" | Score all active clients on health dimensions |
| "Capacity check" | Show team utilization and available hours |
| "Chase overdue invoices" | Generate appropriate follow-up for each aging bucket |
| "QBR for [client]" | Generate quarterly review deck |
| "Agency dashboard" | Compile weekly metrics from all sources |
| "Scope creep alert" | List all unpriced change requests across projects |
| "Growth plan" | Analyze current metrics and recommend next growth lever |
