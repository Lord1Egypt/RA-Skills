---
name: financial-investment-banking
version: 1.0.0
description: Investment banking productivity tools: client and market insights, deck creation, financial analysis, and transaction management
source: anthropics/financial-services
---

# investment-banking

Investment banking productivity tools: client and market insights, deck creation, financial analysis, and transaction management

## 来源
来自 Anthropic 官方 financial-services 仓库的 investment-banking 插件。
原始仓库: https://github.com/anthropics/financial-services

## 可用命令 (Commands)

### buyer-list

---
description: Build a buyer universe for a sell-side process
argument-hint: "[company or sector]"
---

Load the `buyer-list` skill and build a universe of potential strategic and financial acquirers.

If a company or sector is provided, use it. Otherwise ask the user for the target company details.


---

### cim

---
description: Draft a Confidential Information Memorandum
argument-hint: "[company name]"
---

Load the `cim-builder` skill and structure a CIM for the specified company.

If a company name is provided, use it. Otherwise ask the user for the target company and available source materials.


---

### deal-tracker

---
description: Track and review live deal pipeline
argument-hint: ""
---

Load the `deal-tracker` skill to review deal status, update milestones, and manage action items across live deals.


---

### merger-model

---
description: Build an accretion/dilution merger model
argument-hint: "[acquirer] acquiring [target]"
---

Load the `merger-model` skill and build a merger consequences analysis.

If acquirer and target are provided, use them. Otherwise ask the user for deal details.


---

### One-Pager Strip Profile Command

---
description: Create a one-page company strip profile using branded PPT template
argument-hint: "[company name or ticker]"
---

# One-Pager Strip Profile Command

Create a professional one-page company strip profile for pitch books and deal materials.

## Workflow

### Step 1: Gather Company Information

If a company name or ticker is provided, use it. Otherwise ask:
- "What company would you like to profile?"

### Step 2: Check for Available PPT Template Skills

**First, check for existing ppt-template skills** in the skills directory:

```bash
ls skills/ | grep -E "ppt-template|brand-guidelines"
```

If template skills exist (e.g., `techcorp-ppt-template`, `gs-brand-guidelines`):
1. List available templates to the user
2. Ask which template to use, or if they want a clean professional format
3. Load the selected template skill with `skill: "[template-name]"`

If no template skills exist, ask:
- "Do you have a branded PowerPoint template file to use? If so, provide the path. Otherwise I'll use a clean professional format."

If a template file is provided:
1. Analyze the template structure to understand layouts
2. Use appropriate layout for one-pager content

### Step 3: Load Strip Profile Skill

Use `skill: "strip-profile"` to execute the profile creation:

1. **Clarify requirements**:
   - Confirm single-slide format (one-pager)
   - Ask about any specific focus areas

2. **Research company data**:
   - Company overview (HQ, founded, employees, leadership)
   - Business 

---

### process-letter

---
description: Draft a process letter or bid instructions
argument-hint: "[IOI or final bid]"
---

Load the `process-letter` skill and draft process correspondence.

If a letter type is specified (IOI, final bid, management meeting invite), use it. Otherwise ask the user what stage the process is in.


---

### teaser

---
description: Draft an anonymous one-page teaser
argument-hint: "[company name]"
---

Load the `teaser` skill and create a blind teaser for the specified company.

If a company name is provided, use it. Otherwise ask the user for the company details to anonymize.


---

## 底层技能 (Skills)

### buyer-list

---
name: buyer-list
description: Build and organize a universe of potential acquirers for sell-side M&A processes. Identifies strategic and financial buyers, assesses fit, and prioritizes outreach. Use when preparing for a sell-side mandate, building a buyer universe, or evaluating potential partners. Triggers on "buyer list", "buyer universe", "potential acquirers", "who would buy this", "strategic buyers", or "financial sponsors".
---

# Buyer List

## Workflow

### Step 1: Understand the Target

- Company description, sector, and business model
- Revenue, EBITDA, and growth profile
- Key assets and capabilities (IP, customer relationships, geographic footprint, team)
- Expected valuation range
- Seller preferences (strategic vs. financial, management continuity, timeline)

### Step 2: Strategic Buyers

Identify strategic acquirers across categories:

**Direct Competitors**
- Companies in the same space that would gain market share
- Rationale: Revenue synergies, eliminate competitor, scale

**Adjacent Players**
- Companies in adjacent markets that could expand into the target's space
- Rationale: Product extension, cross-sell, new market entry

**Vertical Integrators**
- Customers or suppliers that could integrate vertically
- Rationale: Supply chain control, margin capture, strategic lock-in

**Platform Builders**
- Large companies building a platform in the space through M&A
- Rationale: Tuck-in acquisition, fill capability gap

For each strategic buyer, assess:

| Buyer | Sector | Revenue | Strategic Fit | Financial Capacity | M&A Track Record | Likelihood | Priority |
|-------|--------|---------|--------------|-------------------|------------------|------------|----------|
| | | | High/Med/Low | | Active/Moderate/None | | A/B/C |

### Step 3: Financial Sponsors

Identify PE/financial buyers:

**Platform Investors**
- Sponsors looking for a new platform in this sector
- Criteria: Fund size, sector focus, deal size range

**Add-on Buyers**
- Sponsors with exis

---

### cim-builder

---
name: cim-builder
description: Structure and draft a Confidential Information Memorandum for sell-side M&A processes. Organizes company information into a professional, investor-ready document with consistent formatting and narrative flow. Use when preparing sell-side materials, drafting a CIM, or organizing company data for a sale process. Triggers on "CIM", "confidential information memorandum", "offering memorandum", "info memo", "draft CIM", or "sell-side materials".
---

# CIM Builder

## Workflow

### Step 1: Gather Source Materials

Ask for available inputs:
- Management presentations
- Historical financials (3-5 years)
- Budget/forecast
- Company website and marketing materials
- Customer data (anonymized if needed)
- Org chart
- Prior presentations or board decks
- Quality of earnings report (if available)

### Step 2: CIM Structure

Standard CIM table of contents:

**I. Executive Summary** (2-3 pages)
- Company overview — what they do, why they win
- Investment highlights (5-7 key selling points)
- Financial summary — headline revenue, EBITDA, growth, margins
- Transaction overview — what's being sold, indicative timeline

**II. Company Overview** (3-5 pages)
- History and founding story
- Mission and value proposition
- Products and services description
- Business model and revenue streams
- Key differentiators and competitive advantages

**III. Industry Overview** (3-5 pages)
- Market size and growth dynamics (TAM/SAM/SOM)
- Key industry trends and tailwinds
- Competitive landscape
- Regulatory environment
- Barriers to entry

**IV. Growth Opportunities** (2-3 pages)
- Organic growth levers (new products, markets, pricing)
- M&A / add-on opportunities
- Operational improvements
- Technology investments
- White space analysis

**V. Customers & Sales** (3-5 pages)
- Customer overview (number, segments, geography)
- Top customer analysis (anonymized if pre-LOI)
- Customer concentration and retention metrics
- Sales process and go-to-market strategy
- Pi

---

### datapack-builder

---
name: datapack-builder
description: Build professional financial services data packs from various sources including CIMs, offering memorandums, SEC filings, web search, or MCP servers. Extract, normalize, and standardize financial data into investment committee-ready Excel workbooks with consistent structure, proper formatting, and documented assumptions. Use for M&A due diligence, private equity analysis, investment committee materials, and standardizing financial reporting across portfolio companies. Do not use for simple financial calculations or working with already-completed data packs.
---

# Financial Data Pack Builder

Build professional, standardized financial data packs for private equity, investment banking, and asset management. Transform financial data from CIMs, offering memorandums, SEC filings, web search, or MCP server access into polished Excel workbooks ready for investment committee review.

**Important:** Use the xlsx skill for all Excel file creation and manipulation throughout this workflow.

## CRITICAL SUCCESS FACTORS

Every data pack must achieve these standards. Failure on any point makes the deliverable unusable.

### 1. Data Accuracy (Zero Tolerance for Errors)
- Trace every number to source document with page reference
- Use formula-based calculations exclusively (no hardcoded values)
- Cross-check subtotals and totals for internal consistency
- Verify balance sheet balances: Assets = Liabilities + Equity
- Confirm cash flow ties to balance sheet changes

### 2. ESSENTIAL RULES

**RULE 1: Financial data (measuring money) → Currency format with $**
Triggers: Revenue, Sales, Income, EBITDA, Profit, Loss, Cost, Expense, Cash, Debt, Assets, Liabilities, Equity, Capex
Format: $#,##0.0 for millions, $#,##0 for thousands
Negatives: $(123.0) NOT -$123

**RULE 2: Operational data (counting things) → Number format, NO $**
Triggers: Units, Stores, Locations, Employees, Customers, Square Feet, Properties, Headcount
Format: #,##0 with commas
Neg

---

### deal-tracker

---
name: deal-tracker
description: Track multiple live deals with milestones, deadlines, action items, and status updates. Maintains a deal pipeline view and surfaces upcoming deadlines and overdue items. Use when managing a book of business, tracking process milestones, or preparing for weekly deal reviews. Triggers on "deal tracker", "deal status", "where are we on", "process update", "deal pipeline", or "weekly deal review".
---

# Deal Tracker

## Workflow

### Step 1: Deal Setup

For each deal, capture:
- **Deal name / code name**: Project [Name]
- **Client**: Seller or buyer name
- **Deal type**: Sell-side, buy-side, financing, restructuring
- **Role**: Lead advisor, co-advisor, fairness opinion
- **Deal size**: Expected enterprise value
- **Stage**: Pre-mandate → Engaged → Marketing → IOI → Diligence → Final bids → Signing → Close
- **Team**: MD, VP, Associate, Analyst assigned
- **Key dates**: Engagement date, CIM distribution, IOI deadline, management meetings, final bid deadline, target close

### Step 2: Milestone Tracking

Track key milestones per deal:

| Milestone | Target Date | Actual Date | Status | Notes |
|-----------|------------|-------------|--------|-------|
| Engagement letter signed | | | | |
| CIM / teaser drafted | | | | |
| Buyer list approved | | | | |
| Teaser distributed | | | | |
| NDA execution | | | | |
| CIM distributed | | | | |
| IOI deadline | | | | |
| IOIs received / reviewed | | | | |
| Shortlist selected | | | | |
| Management meetings | | | | |
| Data room opened | | | | |
| Final bid deadline | | | | |
| Bids received / reviewed | | | | |
| Exclusivity granted | | | | |
| Confirmatory diligence | | | | |
| Purchase agreement signed | | | | |
| Regulatory approval | | | | |
| Close | | | | |

Status: On Track / At Risk / Delayed / Complete

### Step 3: Action Items

Maintain a running action item list across all deals:

| Action | Deal | Owner | Due Date | Priority | Status |
|--------|------|-------|----------|----------|

---

### merger-model

---
name: merger-model
description: Build accretion/dilution analysis for M&A transactions. Models pro forma EPS impact, synergy sensitivities, and purchase price allocation. Use when evaluating a potential acquisition, preparing merger consequences analysis for a pitch, or advising on deal terms. Triggers on "merger model", "accretion dilution", "M&A model", "pro forma EPS", "merger consequences", or "deal impact analysis".
---

# Merger Model

## Workflow

### Step 1: Gather Inputs

**Acquirer:**
- Company name, current share price, shares outstanding
- LTM and NTM EPS (GAAP and adjusted)
- P/E multiple
- Pre-tax cost of debt, tax rate
- Cash on balance sheet, existing debt

**Target:**
- Company name, current share price, shares outstanding (if public)
- LTM and NTM EPS or net income
- Enterprise value or equity value

**Deal Terms:**
- Offer price per share (or premium to current)
- Consideration mix: % cash vs. % stock
- New debt raised to fund cash portion
- Expected synergies (revenue and cost) and phase-in timeline
- Transaction fees and financing costs
- Expected close date

### Step 2: Purchase Price Analysis

| Item | Value |
|------|-------|
| Offer price per share | |
| Premium to current | |
| Equity value | |
| Plus: net debt assumed | |
| Enterprise value | |
| EV / EBITDA implied | |
| P/E implied | |

### Step 3: Sources & Uses

| Sources | $ | Uses | $ |
|---------|---|------|---|
| New debt | | Equity purchase price | |
| Cash on hand | | Refinance target debt | |
| New equity issued | | Transaction fees | |
| | | Financing fees | |
| **Total** | | **Total** | |

### Step 4: Pro Forma EPS (Accretion / Dilution)

Calculate year-by-year (Year 1-3):

| | Standalone | Pro Forma | Accretion/(Dilution) |
|---|-----------|-----------|---------------------|
| Acquirer net income | | | |
| Target net income | | | |
| Synergies (after tax) | | | |
| Foregone interest on cash (after tax) | | | |
| New debt interest (after tax) | | | |
| Intangible amortizat

---

### pitch-deck

---
name: pitch-deck
description: "Populates investment banking pitch deck templates with data from source files. Use when: user provides a PowerPoint template to fill in, user has source data (Excel/CSV) to populate into slides, user mentions populating or filling a pitch deck template, or user needs to transfer data into existing slide layouts. Not for creating presentations from scratch."
---

# Populating Investment Banking Pitch Deck Templates

## Reference Files

**Read all reference files at task start before beginning any work.** These contain critical patterns and anti-patterns that will affect your approach. Do not wait until you encounter issues.

| File | Purpose |
|------|---------|
| [`formatting-standards.md`](reference/formatting-standards.md) | Text, bullets, tables, charts, alignment |
| [`slide-templates.md`](reference/slide-templates.md) | Content mapping guidance for common slide types |
| [`xml-reference.md`](reference/xml-reference.md) | PowerPoint XML patterns for tables, shapes, arrows |
| [`calculation-standards.md`](reference/calculation-standards.md) | Financial formulas for verification (CAGR, consensus) |

---

## Workflow Decision Tree

**What type of task is this?**

```
┌─ Populating empty template with source data?
│  └─→ Follow "Template Population Workflow" below
│
├─ Editing existing populated slides?
│  └─→ Extract current content, modify, revalidate
│
└─ Fixing formatting issues on existing slides?
   └─→ See "Common Failures" table, apply targeted fixes
```

---

## ⚠️ Critical Rendering Limitation

**LibreOffice is used for validation but DOES NOT render PowerPoint files accurately.** It will mangle fonts, gradients, shape positions, text wrapping, and some table formatting.

**What this means:** A slide that passes visual validation in LibreOffice may still have issues in Microsoft PowerPoint. The validation loop catches structural issues (missing content, broken tables, placeholder formatting retained) but **cannot** catch 

---

### process-letter

---
name: process-letter
description: Draft process letters and bid instructions for sell-side M&A processes. Covers initial indication of interest (IOI) instructions, final bid procedures, and management meeting logistics. Triggers on "process letter", "bid instructions", "IOI letter", "bid procedures", "final round letter", or "management meeting invite".
---

# Process Letter

## Workflow

### Step 1: Determine Letter Type

- **Initial process letter**: Sent with teaser/CIM to outline the process and IOI requirements
- **IOI instructions**: Specific requirements for first-round indications of interest
- **Second round / final bid letter**: Instructions for submitting binding offers after diligence
- **Management meeting invitation**: Logistics for in-person management presentations

### Step 2: Initial Process Letter / IOI Instructions

**Header:**
- Date, deal code name
- "Confidential"
- Addressed to prospective buyer

**Sections:**

1. **Introduction**: Brief overview of the opportunity and the seller's objectives
2. **Process Overview**: Timeline, key dates, expected number of rounds
3. **IOI Requirements**: What to include in the initial indication:
   - Proposed valuation range (enterprise value)
   - Consideration form (cash, stock, earnout, rollover)
   - Financing sources and certainty
   - Key due diligence requirements
   - Indicative timeline to close
   - Any conditions or contingencies
   - Brief description of the buyer and strategic rationale
4. **Submission Details**: Where to send, deadline (date and time), format
5. **Confidentiality Reminder**: Reference to NDA, data room access
6. **Contact Information**: Banker contacts for questions

### Step 3: Final Bid / Second Round Letter

Additional requirements beyond IOI:

1. **Markup of purchase agreement**: Provide the draft SPA/APA and request markup
2. **Detailed financing commitments**: Committed financing letters required
3. **Remaining diligence items**: Specify what confirmatory diligence is

---

### strip-profile

---
name: fsi-strip-profile
description: |
  Creates professional investment banking strip profiles (company profiles) for pitch books, deal materials, and client presentations. Generates 1-4 information-dense slides with quadrant layouts, charts, and tables.
---

## Workflow

### 1. Clarify Requirements
- **Ask the user**: Single-slide or multi-slide (3-4 slides)?
- **Ask the user**: Any specific focus areas or topics to emphasize?
- **Only after user confirms**, proceed to research

### 2. Research & Planning
**Data Sources:**
- **Primary**: Company filings (BamSEC, SEC EDGAR - "Item 1. Business", MD&A), investor presentations, corporate website
- **Market data**: Bloomberg, FactSet, CapIQ (price, shares, market cap, net debt, EV, ownership)
- **Estimates**: FactSet/CapIQ consensus for NTM revenue, EBITDA, EPS
- **News**: Press releases from last 90 days, M&A activity, guidance changes

**Required Metrics:**
- **Financials**: Revenue, EBITDA, margins (%), EPS, FCF for ±3 years
- **Valuation**: Market Cap, EV, EV/Revenue, EV/EBITDA, P/E multiples
- **Growth**: YoY growth rates (%)
- **Ownership**: Top 5 shareholders with % ownership
- **Segments**: Product mix and/or geographic mix (% breakdown)

**Normalization:**
- Convert all amounts to consistent currency
- Scale consistently ($mm or $bn throughout, not mixed)

**Before Building:**
- Print outline to chat with 4-5 bullet points per item (actual numbers, no placeholders)
- Print style choices: fonts, colors (hex codes), chart types for each data set
- Get user alignment: "Does this outline and visual strategy align with your vision?"

### 3. Slide-by-Slide Creation
**CRITICAL: You MUST create ONE slide at a time and get user approval before proceeding to the next slide.**

**For EACH slide:**
1. Create ONLY this one slide with PptxGenJS
2. **MANDATORY: Convert to image for review** - You MUST convert slides to images so you can visually verify them:
   ```bash
   soffice --headless --convert-to pdf presentation.

---

### teaser

---
name: teaser
description: Draft anonymous one-page company teasers for sell-side M&A processes. Creates a compelling summary without revealing the company's identity, designed to gauge buyer interest before NDA execution. Triggers on "teaser", "blind teaser", "anonymous profile", "one-pager for process", or "draft teaser for sell-side".
---

# Teaser

## Workflow

### Step 1: Gather Inputs

- Company description (what they do, how they make money)
- Sector / industry
- Key financial metrics: revenue, EBITDA, growth rate, margins
- Geographic footprint
- Key selling points (3-5 highlights)
- What to anonymize vs. disclose
- Target buyer audience (strategic, financial, or both)

### Step 2: Teaser Structure

One page, professionally formatted:

**Header**
- Deal code name (e.g., "Project [Name]")
- Sector descriptor (e.g., "Leading Specialty Industrial Services Platform")
- "Confidential — For Discussion Purposes Only"

**Company Description** (2-3 sentences)
- What the company does, without naming it
- Market position (e.g., "a leading provider of...", "a top-3 player in...")
- Geography (region-level, not city-specific)

**Investment Highlights** (4-6 bullet points)
- Market leadership / positioning
- Revenue quality (recurring %, retention, diversification)
- Growth profile and trajectory
- Margin profile and expansion opportunity
- Management team strength
- Strategic value / synergy potential

**Financial Summary** (table or key metrics)

| Metric | Value |
|--------|-------|
| Revenue | $XXM |
| Revenue Growth | XX% CAGR |
| EBITDA | $XXM |
| EBITDA Margin | XX% |
| Employees | XXX |

**Transaction Overview** (2-3 sentences)
- What's being offered (100% sale, majority stake, growth equity)
- Indicative timeline
- Contact information for expressions of interest

### Step 3: Anonymization Check

Ensure the teaser doesn't inadvertently identify the company:
- No company name, brand names, or product names
- No specific city (use region: "Southeast US", "Midwest

---
