---
name: financial-private-equity
version: 1.0.0
description: Private equity deal sourcing and workflow tools: company discovery, CRM integration, and founder outreach
source: anthropics/financial-services
---

# private-equity

Private equity deal sourcing and workflow tools: company discovery, CRM integration, and founder outreach

## 来源
来自 Anthropic 官方 financial-services 仓库的 private-equity 插件。
原始仓库: https://github.com/anthropics/financial-services

## 可用命令 (Commands)

### ai-readiness

---
description: Scan the portfolio for the highest-leverage AI opportunities
argument-hint: "[path to quarterly materials folder, or company names]"
---

Load the `ai-readiness` skill and scan portfolio companies for AI leverage — per-company go / no-go gate, quick wins ranked by EBITDA impact across the portfolio, and replays that hit multiple companies at once.

If a folder or company list is provided, use it. Otherwise ask which companies to include and for their latest quarterly materials.


---

### dd-checklist

---
description: Generate a due diligence checklist
argument-hint: "[company name]"
---

Load the `dd-checklist` skill and generate a comprehensive, sector-tailored due diligence checklist with status tracking.

If a company name is provided, use it. Otherwise ask the user for the target company and deal details.


---

### dd-prep

---
description: Prep for a diligence meeting or expert call
argument-hint: "[company name] [meeting type]"
---

Load the `dd-meeting-prep` skill and generate targeted questions, benchmarks, and red flags to probe.

If details are provided, use them. Otherwise ask for the company, meeting type (management presentation, expert call, customer reference), and topic focus.


---

### ic-memo

---
description: Draft an investment committee memo
argument-hint: "[company name]"
---

Load the `ic-memo` skill and draft a structured IC memo synthesizing due diligence findings, financial analysis, and deal terms.

If a company name is provided, use it. Otherwise ask the user for the target and available materials.


---

### portfolio

---
description: Review portfolio company performance
argument-hint: "[company name or path to financial package]"
---

Load the `portfolio-monitoring` skill and analyze a portfolio company's performance against plan — KPIs, variances, and red flags.

If a company name or file is provided, use it. Otherwise ask the user for the portfolio company and financial data.


---

### returns

---
description: Build IRR/MOIC sensitivity tables
argument-hint: "[company or deal parameters]"
---

Load the `returns-analysis` skill and model PE returns with sensitivity across entry multiple, leverage, exit multiple, and growth scenarios.

If deal parameters are provided, use them. Otherwise ask the user for entry EBITDA, valuation, and financing assumptions.


---

### screen-deal

---
description: Screen an inbound deal (CIM or teaser)
argument-hint: "[path to CIM/teaser file]"
---

Load the `deal-screening` skill and quickly evaluate an inbound deal against the fund's investment criteria.

If a file path is provided, use it. Otherwise ask the user for the deal materials or description.


---

### source

---
description: Source deals — discover companies and draft founder outreach
argument-hint: "[sector or criteria, e.g. 'industrial services in Texas $10-50M']"
---

Load the `deal-sourcing` skill and run the sourcing pipeline: discover target companies, check CRM for existing relationships, and draft personalized founder outreach emails.

If criteria are provided, use them. Otherwise ask the user for sector, size, geography, and deal parameters.


---

### unit-economics

---
description: Analyze unit economics (ARR cohorts, LTV/CAC, retention)
argument-hint: "[company name or path to data]"
---

Load the `unit-economics` skill and analyze customer economics, ARR cohorts, net retention, and revenue quality.

If a company or file is provided, use it. Otherwise ask the user for the target and available data.


---

### value-creation

---
description: Build a post-acquisition value creation plan
argument-hint: "[company name]"
---

Load the `value-creation-plan` skill and structure a value creation roadmap with EBITDA bridge, 100-day plan, and KPI dashboard.

If a company name is provided, use it. Otherwise ask the user for the target company details.


---

## 底层技能 (Skills)

### ai-readiness

---
name: ai-readiness
description: Scan the portfolio for the highest-leverage AI opportunities and rank where to deploy operating-partner time. Ingests quarterly updates and financials across multiple portfolio companies, identifies quick wins at each, and stacks them into a single ranked action list. Use during quarterly portfolio reviews, annual planning, or when deciding which companies get AI investment first. Triggers on "AI readiness", "AI opportunity scan", "where should we deploy AI", "AI across the portfolio", "AI quick wins", or "which portcos are ready for AI".
---

# Portfolio AI Readiness

## Workflow

### Step 1: Connect to Portfolio Data

First, ask the user where the portfolio materials live. Don't assume — offer the options:

- **MCP servers** — data room, SharePoint, Google Drive, or a portfolio-ops database if one is connected
- **Local files** — a folder path on disk with quarterly decks, financials, board packs
- **File uploads** — drag PDFs, PowerPoint, or Excel directly into the conversation

Once connected, pull quarterly updates, board decks, and financials for the portfolio (or a subset). For each company, extract: sector, revenue, headcount by function, tech stack mentioned, and any AI/automation initiatives already in flight.

If the user provides a single company, still run the scan but skip the cross-portfolio ranking.

Ask up front if not obvious from materials:
- Hold period remaining per company (AI payback matters less 12 months from exit)
- Whether any portco has already deployed something that worked

### Step 2: Per-Company Scan

For each company, answer three gate questions. All three yes → **Go**. Any no → **Wait** with a note on what unblocks it.

1. **Is the data there?** Can they produce a clean input for the use case — customer list, invoice feed, contract repository — without a 6-month data project first?
2. **Is there an owner?** Someone on the management team who will drive this, not a sponsor who will "support" it.
3.

---

### dd-checklist

---
name: dd-checklist
description: Generate and track comprehensive due diligence checklists tailored to the target company's sector, deal type, and complexity. Covers all major workstreams with request lists, status tracking, and red flag escalation. Use when kicking off diligence, organizing a data room review, or tracking outstanding items. Triggers on "dd checklist", "due diligence tracker", "diligence request list", "what do we still need", or "data room review".
---

# Due Diligence Checklist

## Workflow

### Step 1: Scope the Diligence

Ask the user for:
- **Target company**: Name, sector, business model
- **Deal type**: Platform acquisition, add-on, growth equity, recap, carve-out
- **Deal size / complexity**: Determines depth of diligence
- **Key concerns**: Any known issues to prioritize (customer concentration, regulatory, environmental, etc.)
- **Timeline**: When is LOI / close targeted?

### Step 2: Generate Workstream Checklists

Generate a checklist across all major workstreams, tailored to the sector:

**Financial Due Diligence**
- Quality of earnings (QoE) — revenue and EBITDA adjustments
- Working capital analysis — normalized vs. actual
- Debt and debt-like items
- Capital expenditure (maintenance vs. growth)
- Tax structure and exposure
- Audit history and accounting policies
- Pro forma adjustments (run-rate, synergies)

**Commercial Due Diligence**
- Market size and growth (TAM/SAM/SOM)
- Competitive positioning and market share
- Customer analysis — concentration, retention, NPS
- Pricing power and contract structure
- Sales pipeline and backlog
- Go-to-market effectiveness

**Legal Due Diligence**
- Corporate structure and org chart
- Material contracts (customer, supplier, partnership)
- Litigation history and pending claims
- IP portfolio and protection
- Regulatory compliance
- Employment agreements and non-competes

**Operational Due Diligence**
- Management team assessment
- Organizational structure and key person risk
- IT systems and

---

### dd-meeting-prep

---
name: dd-meeting-prep
description: Prepare for due diligence meetings — management presentations, expert network calls, customer references, and advisor sessions. Generates targeted question lists, benchmarks to reference, and red flags to probe. Use before any diligence meeting or call. Triggers on "prep for management meeting", "diligence call prep", "expert call questions", "customer reference questions", or "meeting prep for [company]".
---

# Diligence Meeting Prep

## Workflow

### Step 1: Meeting Context

Ask the user for:
- **Meeting type**: Management presentation, expert call, customer reference, advisor check-in, site visit
- **Attendees**: Who from the target company or third party
- **Topic focus**: Full business overview, or specific workstream (financial, commercial, operational, tech)
- **What you already know**: Prior meetings, CIM, data room findings
- **Key concerns**: Specific issues to probe

### Step 2: Generate Question List

Organize questions by priority and topic. Structure depends on meeting type:

#### Management Presentation
**Business Overview (warm-up)**
- Walk us through the founding story and key milestones
- How do you describe the business to someone unfamiliar with the space?
- What are you most proud of? What would you do differently?

**Revenue & Growth**
- Walk us through revenue by customer/segment/geography
- What's driving growth? Price vs. volume vs. new customers
- What does the sales cycle look like? How has win rate trended?
- Where do you see the biggest growth opportunities in the next 3-5 years?

**Competitive Positioning**
- Who do you lose deals to and why?
- What's your moat? How defensible is it?
- How do customers evaluate you vs. alternatives?

**Operations & Team**
- Walk us through the org chart — who are the key people?
- What roles are you hiring for? What's been hardest to fill?
- What keeps you up at night operationally?

**Financial Deep-Dive**
- Walk us through the margin bridge — what's changed and 

---

### deal-screening

---
name: deal-screening
description: Quickly screen inbound deal flow — CIMs, teasers, and broker materials — against the fund's investment criteria. Extracts key deal metrics, runs a pass/fail framework, and outputs a one-page screening memo. Use when reviewing new deal flow, triaging inbound materials, or deciding whether to take a first call. Triggers on "screen this deal", "review this CIM", "should we look at this", "triage this teaser", or "deal screening".
---

# Deal Screening

## Workflow

### Step 1: Extract Deal Facts

From the provided CIM, teaser, or description, extract:

- **Company**: Name, location, sector/subsector
- **Description**: What they do (1-2 sentences)
- **Financials**: Revenue, EBITDA, margins, growth rate
- **Deal type**: Platform, add-on, recap, minority, carve-out
- **Asking price / valuation**: Multiple, enterprise value if stated
- **Seller motivation**: Why selling now
- **Management**: Rolling or exiting
- **Key customers**: Concentration risk
- **Key risks**: Obvious red flags

### Step 2: Screen Against Criteria

Apply the fund's investment criteria (ask user if not known):

| Criterion | Target | Actual | Pass/Fail |
|-----------|--------|--------|-----------|
| Revenue range | | | |
| EBITDA range | | | |
| EBITDA margin | | | |
| Growth profile | | | |
| Sector fit | | | |
| Geography | | | |
| Deal size / EV | | | |
| Valuation (x EBITDA) | | | |
| Customer concentration | | | |
| Management continuity | | | |

### Step 3: Quick Assessment

Provide a 3-part assessment:

1. **Verdict**: Pass / Further Diligence / Hard Pass
2. **Bull case** (2-3 bullets): Why this could be a good deal
3. **Bear case** (2-3 bullets): Key risks and concerns
4. **Key questions**: What you'd need to answer on a first call

### Step 4: Output

One-page screening memo suitable for sharing with partners or an IC quick screen.

## Important Notes

- Speed matters — screening should take minutes, not hours
- Be direct about red flags. Don't bury conce

---

### deal-sourcing

---
name: deal-sourcing
description: PE deal sourcing workflow — discover target companies, check CRM for existing relationships, and draft personalized founder outreach emails. Use when sourcing new deals, prospecting companies in a sector, or reaching out to founders. Triggers on "find companies", "source deals", "draft founder email", "check if we've seen this company", or "outreach to founder".
---

# Deal Sourcing

## Workflow

This skill follows a 3-step sourcing pipeline:

### Step 1: Discover Companies

Research and identify potential target companies based on the user's criteria:

- **Sector/industry focus**: Ask the user what space they're looking in (e.g., "B2B SaaS in healthcare", "industrial services in the Southeast")
- **Deal parameters**: Revenue range, EBITDA range, growth profile, geography, ownership type (founder-owned, PE-backed, corporate carve-out)
- **Sources**: Use web search to find companies matching criteria. Look at industry reports, conference attendee lists, trade publications, and competitor landscapes
- **Output**: A shortlist of companies with: name, description, estimated revenue/size, location, founder/CEO name, website, and why they fit the thesis

### Step 2: CRM Check

Before outreach, check if the company or founder already exists in the firm's CRM:

- Search the user's email (Gmail) for prior correspondence with the company or founder
- Search Slack for any internal mentions or prior discussions about the target
- Ask the user: "Have you or your team had any prior contact with [Company]?"
- Flag any existing relationships, prior passes, or known context
- **Output**: For each company, note: "New" (no prior contact), "Existing" (prior correspondence found — summarize), or "Previously Passed" (if evidence of a prior pass)

### Step 3: Draft Founder Outreach

Draft personalized cold emails to founders/CEOs:

- **Tone**: Professional but warm. Not overly formal — founders respond better to genuine, concise outreach
- **Structure*

---

### ic-memo

---
name: ic-memo
description: Draft a structured investment committee memo for PE deal approval. Synthesizes due diligence findings, financial analysis, and deal terms into a professional IC-ready document. Use when preparing for investment committee, writing up a deal, or creating a formal recommendation. Triggers on "write IC memo", "investment committee memo", "deal write-up", "prepare IC materials", or "recommendation memo".
---

# Investment Committee Memo

## Workflow

### Step 1: Gather Inputs

Collect from the user (or from prior analysis in the session):

- Company overview and business description
- Industry/market context
- Historical financials (3-5 years)
- Management assessment
- Deal terms (price, structure, financing)
- Due diligence findings (commercial, financial, legal, operational)
- Value creation plan / 100-day plan
- Returns analysis (base, upside, downside)

### Step 2: Draft Memo Structure

Standard IC memo format:

**I. Executive Summary** (1 page)
- Company description, deal rationale, key terms
- Recommendation and headline returns
- Top 3 risks and mitigants

**II. Company Overview** (1-2 pages)
- Business description, products/services
- Customer base and go-to-market
- Competitive positioning
- Management team

**III. Industry & Market** (1 page)
- Market size and growth
- Competitive landscape
- Secular trends / tailwinds
- Regulatory environment

**IV. Financial Analysis** (2-3 pages)
- Historical performance (revenue, EBITDA, margins, cash flow)
- Quality of earnings adjustments
- Working capital analysis
- Capex requirements

**V. Investment Thesis** (1 page)
- Why this is an attractive investment (3-5 pillars)
- Value creation levers (organic growth, margin expansion, M&A, multiple expansion)
- 100-day priorities

**VI. Deal Terms & Structure** (1 page)
- Enterprise value and implied multiples
- Sources & uses
- Capital structure / leverage
- Key legal terms

**VII. Returns Analysis** (1 page)
- Base, upside, and downside scenari

---

### portfolio-monitoring

---
name: portfolio-monitoring
description: Track and analyze portfolio company performance against plan. Ingests monthly/quarterly financial packages (Excel, PDF), extracts KPIs, flags variances to budget, and produces summary dashboards. Use when reviewing portfolio company financials, preparing board materials, or monitoring covenant compliance. Triggers on "review portfolio company", "monthly financials", "how is [company] performing", "covenant check", or "portfolio update".
---

# Portfolio Monitoring

## Workflow

### Step 1: Ingest Financial Package

- Accept the user's portfolio company financial package (Excel workbook, PDF, or CSV)
- Extract key financials: Revenue, EBITDA, cash balance, debt outstanding, capex, working capital
- Identify the reporting period and compare to prior period and budget/plan

### Step 2: KPI Extraction & Variance Analysis

Key metrics to track (adapt to the company's sector):

**Financial KPIs:**
- Revenue vs. budget ($ and %)
- EBITDA and EBITDA margin vs. budget
- Cash balance and net debt
- Leverage ratio (Net Debt / LTM EBITDA)
- Interest coverage ratio
- Capex vs. budget
- Free cash flow

**Operational KPIs** (ask user or infer from data):
- Customer count / revenue per customer
- Employee headcount / revenue per employee
- Backlog / pipeline
- Churn / retention rates

### Step 3: Flag & Summarize

- **Green**: Within 5% of plan
- **Yellow**: 5-15% below plan — flag for discussion
- **Red**: >15% below plan or covenant breach risk — immediate attention

Output a concise summary:
1. One-paragraph executive summary ("Company X is tracking [ahead/behind/on] plan...")
2. KPI table with actual vs. budget vs. prior period
3. Red/yellow flags with context
4. Covenant compliance status (if applicable)
5. Questions for management

### Step 4: Trend Analysis

If multiple periods are provided:
- Chart key metrics over time (revenue, EBITDA, cash)
- Identify trends — accelerating, decelerating, or stable
- Compare vs. underwriting cas

---

### returns-analysis

---
name: returns-analysis
description: Build quick IRR/MOIC sensitivity tables for PE deal evaluation. Models returns across entry multiple, leverage, exit multiple, growth, and hold period scenarios. Use when sizing up a deal, stress-testing assumptions, or preparing IC returns exhibits. Triggers on "returns analysis", "IRR sensitivity", "MOIC table", "what's the return at", "model the returns", or "back of the envelope".
---

# Returns Analysis

## Workflow

### Step 1: Gather Deal Inputs

Ask for (or extract from prior analysis):

**Entry:**
- Entry EBITDA (LTM or NTM)
- Entry multiple (EV / EBITDA)
- Enterprise value
- Net debt at close
- Equity check size
- Transaction fees & expenses

**Financing:**
- Senior debt (x EBITDA, rate, amortization)
- Subordinated debt / mezzanine (if any)
- Total leverage at entry (x EBITDA)
- Equity contribution

**Operating Assumptions:**
- Revenue growth rate (annual)
- EBITDA margin trajectory
- Capex as % of revenue
- Working capital changes
- Debt paydown schedule

**Exit:**
- Hold period (years)
- Exit multiple (EV / EBITDA)
- Exit EBITDA (calculated from growth assumptions)

### Step 2: Base Case Returns

Calculate:

| Metric | Value |
|--------|-------|
| Entry EV | |
| Equity invested | |
| Exit EBITDA | |
| Exit EV | |
| Net debt at exit | |
| Exit equity value | |
| **MOIC** | |
| **IRR** | |
| Cash-on-cash | |

Show the returns waterfall:
- EBITDA growth contribution
- Multiple expansion/contraction contribution
- Debt paydown contribution
- Fee/expense drag

### Step 3: Sensitivity Tables

Build 2-way sensitivity matrices:

**Entry Multiple vs. Exit Multiple**
| | Exit 6x | Exit 7x | Exit 8x | Exit 9x | Exit 10x |
|---|---------|---------|---------|---------|----------|
| Entry 7x | | | | | |
| Entry 8x | | | | | |
| Entry 9x | | | | | |
| Entry 10x | | | | | |

**EBITDA Growth vs. Exit Multiple** (at fixed entry)

**Leverage vs. Exit Multiple** (at fixed entry and growth)

**Hold Period vs. Exit Multiple**

Show bot

---

### unit-economics

---
name: unit-economics
description: Analyze unit economics for PE targets — ARR cohorts, LTV/CAC, net retention, payback periods, revenue quality, and margin waterfall. Essential for software/SaaS, recurring revenue, and subscription businesses. Use when evaluating revenue quality, building a cohort analysis, or assessing customer economics. Triggers on "unit economics", "cohort analysis", "ARR analysis", "LTV CAC", "net retention", "revenue quality", or "customer economics".
---

# Unit Economics Analysis

## Workflow

### Step 1: Identify Business Model

Determine the revenue model to tailor the analysis:
- **SaaS / Subscription**: ARR, net retention, cohorts
- **Recurring services**: Contract value, renewal rates, upsell
- **Transaction / usage-based**: Revenue per transaction, volume trends, take rate
- **Hybrid**: Break down by revenue stream

### Step 2: Core Metrics

#### ARR / Revenue Quality
- **ARR bridge**: Beginning ARR → New → Expansion → Contraction → Churn → Ending ARR
- **ARR by cohort**: Vintage analysis — how does each annual cohort retain and grow?
- **Revenue concentration**: Top 10/20/50 customers as % of total
- **Revenue by type**: Recurring vs. non-recurring vs. professional services
- **Contract structure**: ACV distribution, multi-year %, auto-renewal %

#### Customer Economics
- **CAC (Customer Acquisition Cost)**: Total S&M spend / new customers acquired
- **LTV (Lifetime Value)**: (ARPU × Gross Margin) / Churn Rate
- **LTV:CAC ratio**: Target >3x for healthy businesses
- **CAC payback period**: Months to recover acquisition cost
- **Blended vs. segmented**: Break down by customer segment (enterprise vs. SMB vs. mid-market)

#### Retention & Expansion
- **Gross retention**: % of beginning ARR retained (excludes expansion)
- **Net retention (NDR)**: % of beginning ARR retained including expansion
- **Logo churn**: % of customers lost
- **Dollar churn**: % of revenue lost (often different from logo churn)
- **Expansion rate**: Upsell + cr

---

### value-creation-plan

---
name: value-creation-plan
description: Structure post-acquisition value creation plans with revenue, cost, and operational levers mapped to an EBITDA bridge. Includes 100-day priorities, KPI targets, and accountability frameworks. Use when planning post-close execution, preparing operating partner materials, or building a board-ready value creation roadmap. Triggers on "value creation plan", "100-day plan", "post-close plan", "EBITDA bridge", "operating plan", or "value creation levers".
---

# Value Creation Plan

## Workflow

### Step 1: Baseline Assessment

Understand the starting point:
- Current revenue, EBITDA, and margins
- Organizational structure and capabilities
- Key operational metrics by function
- Management team strengths and gaps
- Quick wins already identified during diligence

### Step 2: Value Creation Levers

Map all levers to an EBITDA bridge over the hold period:

#### Revenue Growth Levers
- **Organic growth**: Price increases, volume growth, market expansion
- **Cross-sell / upsell**: New products to existing customers
- **New market entry**: Geographic expansion, new verticals, new channels
- **Sales force effectiveness**: Hire reps, improve conversion, shorten cycle
- **M&A / add-ons**: Bolt-on acquisitions to add revenue and capabilities

For each lever:
- Current state → Target state
- Revenue impact ($)
- Timeline to impact
- Investment required
- Confidence level (high/medium/low)

#### Margin Expansion Levers
- **Pricing optimization**: Price increases, mix shift, bundling
- **COGS reduction**: Procurement savings, supplier consolidation, automation
- **OpEx optimization**: Overhead reduction, shared services, offshoring
- **Technology investment**: Automation, systems integration, data analytics
- **Scale leverage**: Fixed cost leverage as revenue grows

#### Strategic / Multiple Expansion
- **Platform building**: Add-on acquisitions, tuck-ins
- **Recurring revenue shift**: Move from project to recurring/subscription
- **Market po

---
