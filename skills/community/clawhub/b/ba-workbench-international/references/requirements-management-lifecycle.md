
## Requirements Management Full Lifecycle

### Five-Stage Requirements Management

```
Elicitation → Analysis → Specification → Validation → Management
```

| Stage | Core Activities | Output | Common Pitfalls |
|-------|----------------|--------|-----------------|
| **Elicitation** | Interviews, workshops, observation, document analysis | Elicitation plan, raw requirements records | Only listening, not observing; ignoring tacit requirements |
| **Analysis** | MECE decomposition, prioritization, conflict resolution | Requirements analysis docs, requirements relationship diagrams | Over-analysis leading to "analysis paralysis" |
| **Specification** | Requirements documentation, modeling, defining acceptance criteria | BRD/FRD/User Stories + AC | Too detailed or too vague |
| **Validation** | Reviews, prototype validation, test case cross-referencing | Validation records, change requests | Skipping requirements review and going straight to development |
| **Management** | Change control, traceability maintenance, status tracking | Requirements traceability matrix, change log | No process for requirements changes; RTM exists in name only |

### Requirements Traceability Matrix (RTM) Template

| ID | Requirement Description | Source | Priority | Linked BRD | Linked FRD | Linked Test Cases | Status |
|----|------------------------|--------|----------|------------|------------|-------------------|--------|
| REQ-001 | ... | Interview - Zhang San | Must | BRD-Ch3 | FRD-2.1 | TC-001, TC-002 | Confirmed |
| REQ-002 | ... | RFP-3.2 | Should | BRD-Ch3 | FRD-2.2 | TC-003 | In Development |

### Requirements Change Control Process

```
Change Request → Impact Analysis → CCB Review → Approve/Reject → Update Baseline → Notify Stakeholders
    (CR)          (Impact)        (Change Control Board)          (Baseline Update)
```

---

### Stage 1: Strategy & Industry Analysis

**Role: Strategy Analyst / Strategy BA**

> "Choice matters more than effort — analyzing in the wrong industry, no matter how good the analysis, is wasted effort."

#### 1.1 Macro Environment Analysis

##### PESTLE Analysis Framework

| Dimension | Key Questions | Data Sources | Analysis Frequency |
|-----------|---------------|-------------|-------------------|
| **P-Political** | Policy/regulatory changes? Government subsidy directions? Trade policies? | Government websites / Policy documents / Think tanks | Continuous tracking |
| **E-Economic** | GDP growth rate? Interest rate trends? Exchange rate fluctuations? Inflation? | Central banks / Statistics bureaus / Bloomberg | Quarterly |
| **S-Social** | Demographics? Consumption habits? Value shifts? | Statistics bureaus / Census / Research reports | Annual |
| **T-Technological** | Disruptive technologies? Technology maturity? R&D investment? | Gartner / Patent databases / Academic papers | Continuous tracking |
| **L-Legal** | Regulatory changes? Compliance requirements? Intellectual property? | Legal databases / Law firm reports | Continuous tracking |
| **E-Environmental** | ESG requirements? Carbon neutrality policies? Sustainable development? | Environmental agencies / ESG reports | Quarterly |

##### PESTLE Analysis Output Format

```
┌─────────────────────────────────────────────┐
│ PESTLE Analysis One-Pager                    │
│                                               │
│ [Political]  [Economic]   [Social]           │
│ ·Key finding 1 ·Key finding 1 ·Key finding 1 │
│ ·Key finding 2 ·Key finding 2 ·Key finding 2 │
│                                               │
│ [Technology] [Legal]      [Environment]       │
│ ·Key finding 1 ·Key finding 1 ·Key finding 1  │
│ ·Key finding 2 ·Key finding 2 ·Key finding 2  │
│                                               │
│ ⚠ Key Uncertainties:                          │
│ 💡 Implications & Insights for Our Side:      │
└─────────────────────────────────────────────┘
```

##### NEST Analysis (Digital Age Alternative to PESTLE)

```
Best for: Digital-native industries (Internet / SaaS / FinTech)

N - Network Effects: Winner-take-all degree?
E - Ecosystem: Platform vs vertical? Where's our niche?
S - Switching Costs: Are user migration costs high?
T - Technology Shift: AI / Web3 / Quantum disruption?

NEST vs PESTLE: More focused on structural factors of the digital economy
```

#### 1.2 Industry Structure Analysis

##### Porter's Five Forces

```
                    Threat of New Entrants
                    (Easy for new competitors to enter?)
                          ↑
    Supplier Bargaining Power → Industry Rivalry Intensity ← Buyer Bargaining Power
    (How strong are suppliers?)  (What's the landscape?)    (How strong are customers?)
                          ↑
                    Threat of Substitutes
                    (Are there alternatives?)
```

| Force | High Score (5) Means | Assessment Dimensions | Score |
|-------|---------------------|----------------------|-------|
| Threat of New Entrants | Easy entry, intensifying competition | Capital barriers / Tech barriers / Economies of scale / Licenses / Brand / Switching costs | |
| Supplier Bargaining Power | Strong suppliers, squeezing profits | Supplier concentration / Alternative supply / Switching costs / Forward integration | |
| Buyer Bargaining Power | Strong customers, pressing prices | Customer concentration / Product differentiation / Switching costs / Backward integration | |
| Threat of Substitutes | High substitution risk | Substitute price-performance / Switching costs / Customer willingness to substitute | |
| Industry Rivalry | Intense competition | Number of competitors / Industry growth / Exit barriers / Fixed cost ratio | |

##### Industry Lifecycle Analysis

```
Introduction → Growth → Shakeout → Maturity → Decline

Strategic focus by stage:
Introduction: Educate market, capture mindshare, rapid iteration
Growth: Land grab, scale first, seize market share ← Best investment window
Shakeout: Differentiate, build brand, eliminate weak players
Maturity: Cost leadership, efficiency improvement, M&A consolidation
Decline: Harvest profits, find new S-curve, transform or exit
```

**Determining Industry Stage:**

| Indicator | Introduction | Growth | Maturity | Decline |
|-----------|-------------|--------|----------|---------|
| Market Growth Rate | Low but accelerating | >20% | 5-10% | <5% or negative |
| Number of Competitors | Few | Rapidly increasing | Stable/decreasing | Exiting |
| Product Differentiation | High | Rapidly converging | Homogeneous | Undifferentiated |
| Profit Levels | Negative | Rapidly improving | Stable/declining | Low |

#### 1.3 Industry Size & Concentration

##### Industry Concentration (CRn / HHI)

```
CR4 (Combined market share of top 4):
>80% → Extremely concentrated (oligopoly): Telecom, power grids, airlines
50-80% → Highly concentrated: Internet platforms, automotive
30-50% → Moderately concentrated: Restaurants, apparel
<30% → Highly fragmented: Housekeeping, legal consulting

HHI (Herfindahl-Hirschman Index = Σ(each firm's market share %)²):
>2500 → Highly concentrated | 1500-2500 → Moderate | <1500 → Fragmented
```

##### Industry Key Success Factors (KSF) Analysis

```
4 Sources for Identifying Industry KSFs:
1. Customer Demand Side → Why do customers choose A over B?
2. Competitive Side → What capability differences exist between winners and losers?
3. Value Chain Side → Which link creates the most value?
4. Structural Factors → What capabilities does the industry's economic characteristics demand?

KSF Matrix:
┌─────────────────┬──────────────────┐
│ Essential but   │ Essential and    │
│ Not Different   │ Differentiating  │
│ (Threshold)     │ (Core Competency)│
├─────────────────┼──────────────────┤
│ Not Important   │ Different but    │
│ (Ignore)        │ Not Essential    │
│                 │ (Nice to Have)   │
└─────────────────┴──────────────────┘
```

#### Deliverables

1. **PESTLE/NEST Analysis Report** (2-3 pages, one-pager with key findings)
2. **Industry Five Forces Analysis** (with scoring + radar chart)
3. **Industry Lifecycle Assessment Report** (with stage identification + strategic recommendations)
4. **Industry KSF Analysis Matrix**

---

### Stage 2: Market & Customer Insight

**Role: Market Analyst / Market Analyst**

> "If you don't know who your customers are, what they want, and how many there are, all business plans are castles in the air."

#### 2.1 Market Segmentation

##### Market Segmentation 5-Dimension Model

| Segmentation Dimension | B2C Indicators | B2B Indicators |
|------------------------|---------------|----------------|
| **Geographic** | City tier / Climate / Population density | HQ location / Regional distribution / Internationalization |
| **Demographic / Firmographic** | Age / Income / Education / Family structure | Industry / Size / Revenue / Employees / Years in business |
| **Psychographic / Strategic** | Lifestyle / Values / Personality | Strategic positioning / Growth stage / Technology maturity |
| **Behavioral / Operational** | Usage frequency / Loyalty / Purchase context | Procurement model / Decision process / Tech stack |
| **Needs / Pain Points** | Jobs-to-be-Done / Use scenarios | Business pain points / Compliance needs / ROI pressure |

##### Market Segmentation Validity Test

```
A good segment must satisfy:
□ Measurable (size, purchasing power quantifiable)
□ Accessible (reachable through channels)
□ Substantial (large enough to warrant dedicated investment)
□ Differentiable (significant differences between segments)
□ Actionable (can design targeted 4P strategies)

MECE Principle Check: Segments are mutually exclusive + collectively exhaustive
```

#### 2.2 Market Sizing (TAM-SAM-SOM)

```
TAM (Total Addressable Market)
→ The ceiling size of your category
→ Formula: Total potential customers × Average annual revenue per customer

SAM (Serviceable Addressable Market)
→ The portion your business model/geography/capabilities can cover
→ Formula: TAM × Reachable proportion

SOM (Serviceable Obtainable Market)
→ What you can realistically capture in 3-5 years
→ Formula: SAM × Reasonable market share

Example: Enterprise SaaS CRM in China
TAM = 40 million enterprises × $1,000/year = $400B
SAM = TAM × 30% (willing to pay + right size) = $120B
SOM = SAM × 5% (reasonable 3-year target) = $6B
```

##### Market Sizing Methodology

| Method | Principle | Applicable | Reliability |
|--------|-----------|------------|-------------|
| **Top-Down** | Start from macro data × penetration rate | New market entry | Medium (tends optimistic) |
| **Bottom-Up** | Aggregate from micro sales data | Already have initial customers | High |
| **Analogy** | Reference similar market/country penetration rates | Innovative categories | Low-Medium |
| **Value Chain** | Derive from supply chain upstream/downstream | Industrial goods / B2B | Medium-High |
| **User Survey** | Survey purchase intent × total market | Consumer new products | Medium |

#### 2.3 Customer Personas & Insights

##### B2B Customer Persona (Enterprise Level)

```
Account Profile:
├── Basic Info: Industry / Size / Revenue / Employees / Years in business / Ownership
├── Technology Profile: Existing systems / Cloud adoption / Tech maturity / IT team size
├── Procurement Profile: Decision makers / Procurement process / Budget cycle / Approval chain
├── Relationship Profile: Supplier relationships / Loyalty / Word-of-mouth influence
└── Needs Profile: Core pain points / Urgency / Budget / Decision criteria

Buyer Persona:
├── Personal Info: Title / Reporting line / KPIs / Career stage
├── Decision Psychology: Risk appetite / Innovation acceptance / Personal goals
├── Information Channels: Industry reports / Peer recommendations / Social media / Conferences
└── Decision Criteria: ROI-first / Security-first / Feature-first / Brand-first
```

##### Customer Journey Analysis

```
B2B Customer 5-Stage Full Journey:
Awareness → Consideration → Evaluation → Purchase → Usage/Renewal

Analysis per stage:
├── What is the customer doing? (Behavior)
├── What is the customer thinking? (Psychology)
├── What are the customer touchpoints? (Channels)
├── What are the customer pain points? (Opportunities)
└── Who needs to be involved? (Internal roles)
```

#### Deliverables

1. **Market Segmentation Report** (with segment profiles + sizing + attractiveness scoring)
2. **TAM-SAM-SOM Sizing Model** (Excel, with methodology + assumptions)
3. **Customer Persona Cards** (B2B version: Account Profile + Buyer Persona)
4. **Customer Journey Map** (with touchpoints, emotions, pain points, opportunities)

---

### Stage 3: Competitive Intelligence & Positioning

**Role: Competitive Intelligence Analyst / CI Analyst**

> "True competitive advantage isn't being stronger than competitors — it's being impossible to replicate."

#### 3.1 Competitive Landscape Panorama

##### Strategic Group Map

```
How to draw:
Select the 2 most important competitive dimensions for the industry
for X and Y axes (e.g., Price vs Quality, Breadth vs Depth, Innovation vs Efficiency)

               High Quality
                ↑
    Premium Niche  |   Premium Full-Line
    (Expensive,    |   (Expensive,
     Focused)      |    Comprehensive)
                   |
  ─────────────────┼─────────────────→ Low Price
                   |
    Economy Niche  |   Mass Value
    (Cheap,        |   (Value for
     Focused)      |    Money)
                   |
              Low Quality

Plot each competitor on the map:
- Bubble size = Market share / Revenue
- Arrow = Strategic movement direction
- Group = Cluster of most closely competing companies
```

##### Competitive Situation Type Assessment

| Situation Type | Characteristics | Strategic Response |
|---------------|-----------------|-------------------|
| **Fragmented Market** | No clear leader, CR4<30% | Scale consolidation, standardization, branding |
| **Emerging Market** | Rapid growth, rules undefined | Occupy position, set standards, educate market |
| **Mature Oligopoly** | CR4>60%, stable competition | Differentiation, efficiency, customer stickiness |
| **Rapid Change** | Technology/business model disruption, old vs new | Agility, continuous innovation, ecosystem building |
| **Winner-Take-All** | Network effects + scale effects drive monopoly | Either be #1 or don't play |

#### 3.2 Competitor Deep Dive

##### Competitive Analysis Iron Triangle

```
         ┌──────────────┐
         │  Product/     │
         │  Service      │
         │  (What)       │
         └──────┬───────┘
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Strategy/ │ │ Capability/│ │ Market    │
│ Vision    │ │ Resources  │ │ Performance│
│ (Why)     │ │ (How)      │ │ (So What)  │
└──────────┘ └──────────┘ └──────────┘
```

##### Competitor Analysis 12-Dimension Framework

| Dimension | Us | Competitor A | Competitor B | Gap |
|-----------|-----|-------------|-------------|-----|
| **Strategy & Vision** | | | | |
| Target Market & Customers | | | | |
| Value Proposition | | | | |
| Growth Strategy | | | | |
| **Product & Service** | | | | |
| Core Features | | | | |
| Differentiating Features | | | | |
| User Experience / Satisfaction | | | | |
| **Business Model** | | | | |
| Revenue Model | | | | |
| Pricing Level | | | | |
| Cost Structure (Estimated) | | | | |
| **Operational Capability** | | | | |
| Supply Chain / Delivery | | | | |
| Organization & Talent | | | | |
| Technology / IT Capability | | | | |
| **Market Performance** | | | | |
| Market Share (Estimated) | | | | |
| Growth Rate | | | | |
| Customer NPS / Word-of-Mouth | | | | |

##### Competitor Signal Collection

```
Primary Intelligence:
├── Purchase competitor products/services (hands-on testing)
├── Competitor customer interviews (Why did they choose them? Why not us?)
├── Competitor ex-employee interviews (LinkedIn outreach)
├── Industry trade shows/conferences (booths + talks + private conversations)
└── Channel partner interviews (distributors/integrators)

Secondary Intelligence:
├── Competitor website / help docs / Changelog
├── Competitor job postings (reverse-engineer tech stack/team size/business direction)
├── Financial reports / prospectuses (if public)
├── App Store / marketplace reviews
├── Social media / tech communities
├── Patent databases
└── Industry reports (Gartner Magic Quadrant / IDC MarketScape / Forrester Wave)
```

#### 3.3 Competitive Positioning & Strategy

##### Porter's Generic Competitive Strategies

```
        Competitive Advantage
        Low Cost    Differentiation
    ┌──────────┬──────────┐
Broad│ Cost     │ Different-│
Target│ Leadership│ iation    │
    │(Walmart) │(Apple)    │
    ├──────────┼──────────┤
Narrow│ Cost    │ Different-│
Target│ Focus   │ iation    │
    │(Costco)  │ Focus     │
    │          │(Ferrari)  │
    └──────────┴──────────┘
```

##### Value Curve Analysis (Blue Ocean Strategy)

```
X-axis: Industry key competitive factors
Y-axis: Investment level (High/Medium/Low)

Steps:
1. List the industry's existing competitive factors (5-8)
2. Plot the value curves of major competitors
3. Ask 4 questions (ERRC Framework):
   ├── Eliminate: Which factors that the industry takes for granted should be eliminated?
   ├── Reduce: Which factors should be reduced well below the industry standard?
   ├── Raise: Which factors should be raised well above the industry standard?
   └── Create: Which factors that the industry has never offered should be created?

Blue Ocean Strategy Test:
→ Is the new value curve focused, unique, and with a compelling tagline?
```

#### Deliverables

1. **Competitive Landscape Overview** (with strategic group map + situation assessment)
2. **Competitor Deep Dive Report** (12-dimension full comparison)
3. **Competitive Positioning Strategy Recommendations** (with value curve + generic strategy choice)
4. **Competitor Intelligence Tracking System** (information sources + update frequency + responsible person)

---

### Stage 4: Financial Analysis & Modeling

**Role: Financial Analyst / Financial Analyst**

> "Numbers don't lie, but they need interpretation. Financial analysis is the axiomatic foundation of business analysis."

#### 4.1 Financial Statement Analysis

##### Three Key Statements — Core Focus

| Statement | Core Question | BA's Key Focus Areas | Key Metrics |
|-----------|--------------|---------------------|-------------|
| **Income Statement** | Is it profitable? | Revenue structure / Gross margin / Expense ratio / Operating margin | Gross Margin / Net Margin / EBITDA |
| **Balance Sheet** | Is it healthy? | Cash / Accounts Receivable / Inventory / Debt structure / Equity | Debt-to-Asset Ratio / Current Ratio / Quick Ratio |
| **Cash Flow Statement** | Is there real cash? | Operating cash flow / Investing cash flow / Financing cash flow | Free Cash Flow / Cash Flow Coverage |

##### DuPont Analysis System

```
ROE (Return on Equity) = Net Profit / Shareholders' Equity
                        = Net Profit Margin × Asset Turnover × Leverage
                        = (Net Profit/Revenue) × (Revenue/Total Assets) × (Total Assets/Shareholders' Equity)

Meaning of ROE Decomposition:
├── High ROE from high margin → Differentiation / Brand / Pricing power companies
├── High ROE from high turnover → Efficiency / Scale companies
├── High ROE from high leverage → Financial / Real estate companies (RISK!)
└── ROE needs 3-5 year trend analysis; single year may be manipulated

Application: Compare ROE and its drivers across competitors to assess different business model quality
```

#### 4.2 Financial Ratio Analysis

```
Profitability:
├── Gross Margin = (Revenue - COGS) / Revenue           → Product/service pricing power
├── Operating Margin = Operating Profit / Revenue        → Operational efficiency
├── Net Margin = Net Profit / Revenue                    → Overall profitability
├── ROE = Net Profit / Shareholders' Equity              → Shareholder returns
├── ROA = Net Profit / Total Assets                      → Asset efficiency
└── ROIC = NOPAT / Invested Capital                      → Investment returns (MOST IMPORTANT!)

Solvency:
├── Current Ratio = Current Assets / Current Liabilities        → >1.5 healthy
├── Quick Ratio = (Current Assets - Inventory) / Current Liabilities → >1.0 healthy
├── Debt-to-Asset Ratio = Total Liabilities / Total Assets      → <60% generally acceptable
└── Interest Coverage = EBIT / Interest Expense                 → >3 safe

Operational Efficiency:
├── Days Sales Outstanding (DSO) = AR / Average Daily Revenue   → Smaller is better
├── Days Inventory Outstanding (DIO) = Inventory / Average Daily COGS → Smaller is better
├── Days Payable Outstanding (DPO) = AP / Average Daily COGS    → Larger is better (within reason)
└── Cash Conversion Cycle (CCC) = DSO + DIO - DPO               → Core operational metric

Growth Capability:
├── Revenue Growth Rate (CAGR 3-year)
├── Profit Growth Rate
└── Sustainable Growth Rate = ROE × (1 - Dividend Payout Ratio)
```

#### 4.3 Valuation Modeling

##### DCF Valuation (Discounted Cash Flow)

```
Enterprise Value = Σ(Future Free Cash Flow / (1+WACC)^t) + Terminal Value/(1+WACC)^n

5-Step Method:
Step 1: Forecast future 5-10 year Free Cash Flow (FCF)
  FCF = EBIT×(1-t) + Depreciation & Amortization - CapEx - Change in Working Capital

Step 2: Calculate WACC (Weighted Average Cost of Capital)
  WACC = E/(E+D)×Ke + D/(E+D)×Kd×(1-t)

Step 3: Calculate Terminal Value
  TV = FCF_last × (1+g) / (WACC - g)        ← Perpetuity growth method
  OR TV = EBITDA_last × multiple              ← Exit multiple method

Step 4: Discount and Sum
  Enterprise Value = Σ(FCF_t/(1+WACC)^t) + TV/(1+WACC)^n

Step 5: Equity Value
  Equity Value = Enterprise Value - Net Debt - Minority Interest
```

##### Comparable Company Valuation

```
Select 5-8 comparable public companies or recent transactions

Common Multiples:
├── EV/EBITDA (most common, excludes capital structure and depreciation differences)
├── P/E (Price-to-Earnings, use when earnings are positive)
├── EV/Revenue (for high-growth/unprofitable companies)
├── P/B (Price-to-Book, for financials/asset-heavy)
└── Industry-specific metrics (e.g., SaaS: EV/ARR × Growth Rate)

Comparable Analysis Steps:
1. Screen for comparable companies
2. Collect financial data and multiples
3. Calculate median/mean/quartiles
4. Adjust for differences in growth/profitability
5. Apply to target company to get valuation range
```

#### 4.4 ROI & Investment Return Analysis

| Metric | Formula | Meaning | Decision Criteria | Applicable |
|--------|---------|---------|-------------------|------------|
| **NPV** | Σ(Future CF/(1+r)^t) - Initial Investment | Net Present Value | >0 feasible | Single project |
| **IRR** | r where NPV=0 | Internal Rate of Return | >WACC feasible | Single project |
| **Payback** | Initial Investment / Annual Cash Flow | Years to recoup | Per company standard | Liquidity assessment |
| **ROI** | (Return - Investment) / Investment | Return on Investment | >0 feasible | General |
| **ROIC** | NOPAT / Invested Capital | Return on Invested Capital | >WACC creates value | Enterprise / Business line |
| **PI** | NPV / Initial Investment | Profitability Index | >1 feasible | Ranking under capital constraints |

#### Deliverables

1. **Financial Analysis Report** (with three-statement analysis + DuPont decomposition + ratio diagnostics)
2. **DCF Valuation Model** (Excel, with 5-10 year forecast + sensitivity analysis)
3. **Comparable Company Valuation Table** (multiple comparison + valuation range)
4. **Investment Return Analysis** (NPV/IRR/Payback/ROI comparison)

---


### Stage 5: Business Model Design & Validation

**Role: Business Model Architect / Business Model Architect**

> "Same product, different business model — 10x difference in valuation."

#### 5.1 Business Model Canvas (BMC)

```
┌────────────┬────────────┬────────────┬────────────┐
│ Key Partners│ Key Activities│ Value Prop  │ Customer    │ Customer    │
│ (KP)       │ (KA)        │ (VP)←Soul   │ Relationships│ Segments   │
│            │             │             │ (CR)        │ (CS)        │
│ Who helps  │ What do you │ What problem│ How do you  │ Who do you  │
│ you succeed?│ do that's   │ do you solve?│ maintain     │ serve?      │
│            │ most important?│            │ relationships?│            │
├────────────┼─────────────┤             ├─────────────┤             │
│            │ Key Resources│             │ Channels    │             │
│            │ (KR)        │             │ (CH)        │             │
│            │             │             │             │             │
│            │ What unique │             │ How do you  │             │
│            │ assets do   │             │ reach       │             │
│            │ you have?   │             │ customers?  │             │
├────────────┴─────────────┴─────────────┴─────────────┴─────────────┤
│ Cost Structure (CS): Where does money go? What costs the most?       │
├─────────────────────────────────────────────────────────────────────┤
│ Revenue Streams (RS): Where does money come from? Why do customers pay?│
└─────────────────────────────────────────────────────────────────────┘
```

#### 5.2 Business Model Type Map

| Type | Description | Examples | Key Success Factors |
|------|-------------|----------|---------------------|
| **Subscription (SaaS)** | Ongoing payment for access | Salesforce / Feishu | High retention (>90%) + High NDR (>100%) |
| **Marketplace** | Match supply and demand, take commission | Meituan / Airbnb | Critical mass + Network effects |
| **Advertising** | Free + ad revenue | TikTok / Google | User volume + Targeting precision |
| **Razor-Blade** | Cheap hardware + expensive consumables | Printers / Nespresso | Ecosystem lock-in + Switching costs |
| **Freemium** | Free basic + paid premium | Dropbox / Trello | Conversion rate + Free cost control |
| **Data Monetization** | Free service → Data → Analytics/Insights | Wind / Bloomberg | Data exclusivity + Analysis depth |
| **License** | One-time/periodic licensing fee | Oracle / SAP | Customer stickiness + Audit deterrence |
| **Outcome-Based** | Charge based on value created for customer | Outcome-based consulting | Attribution + Trust + Quantification |
| **Ecosystem Platform** | API/Plugin/Developer ecosystem | Salesforce AppExchange | Critical developer mass + Transaction volume |

#### 5.3 Business Model Validation

##### Lean Canvas — Rapid Validation

```
Unlike BMC (comprehensive but static), Lean Canvas focuses on uncertainty hypothesis testing:

Problem (TOP 3) → Solution → Unique Value Proposition → Unfair Advantage → Customer Segments
      ↑                                                    ↓
Existing Alternatives                                  Key Metrics
                                                        ↓
                                               Channels → Early Adopters
                                                        ↓
Cost Structure ←←←←←←←←←←←←←←←←←←←←←←←←→ Revenue Streams

Core Validation Logic:
1. List the most critical assumptions (Demand assumption > Growth assumption > Profit assumption)
2. Design minimum-cost validation experiments for each assumption
3. Experiment → Data → Falsify or Validate → Iterate
4. First validate Problem-Solution Fit → then Product-Market Fit → finally Scale Fit
```

##### Business Model Stress Test

```
□ Does the customer really have this pain point? (Demand authenticity)
□ How much is the customer willing to pay? (Willingness to pay)
□ Is Customer Acquisition Cost (CAC) reasonable? Can it be recouped? (Unit economics)
□ Is LTV/CAC > 3? (Sustainable growth)
□ Is gross margin sufficient to support the business model? (Profit foundation)
□ Is the market size large enough? (Growth space)
□ Why aren't competitors doing this? (Are there invisible barriers?)
□ Reverse thinking: If this model fails, what is the most likely reason?
```

#### Deliverables

1. **Business Model Canvas (BMC)** (one-pager, 9 modules complete)
2. **Business Model Comparison Analysis** (Us vs Competitors, multi-dimension comparison)
3. **Unit Economics Model** (CAC / LTV / Gross Margin / Contribution Margin)
4. **Hypothesis Validation Plan** (Key assumptions → Validation experiments → Success criteria)

---

### Stage 6: Stakeholder Management

**Role: Stakeholder Manager / Stakeholder Manager**

> "No matter how good the solution, if key stakeholders don't buy in, it's waste paper."

#### 6.1 Stakeholder Identification

##### 5-Dimension Identification Method

| Dimension | Identification Question | Output |
|-----------|------------------------|--------|
| **Decision Authority** | Who has the power to approve/reject this decision? | Decision chain |
| **Influence** | Who, though without formal authority, can sway the decision-maker? | Influencer map |
| **Resources** | Who controls the resources the project needs (budget/people/data)? | Resource holder list |
| **Expertise** | Who possesses the domain knowledge we need? | Expert list |
| **Affected** | Who will be impacted by this change (positively/negatively)? | Impact scope diagram |

##### B2B Typical Stakeholder Panorama

```
C-Suite: CEO / CFO / COO / CIO / CDO
    ↓ Strategic direction + Budget
Business Leaders: BU Head / VP / Director
    ↓ Business requirements + Acceptance
Business Operators: Frontline staff / Operators / Approvers
    ↓ Actual operations + Feedback
IT / Technology: CTO / Architects / Development team
    ↓ Technical feasibility + Implementation
Support Functions: HR / Finance / Legal / Compliance / Procurement
    ↓ Approval + Resources + Compliance
External: Customers / Suppliers / Partners / Regulators
    ↓ Requirements + Constraints + Compliance
```

#### 6.2 Stakeholder Analysis Matrix

##### Power-Interest Grid

```
                Power / Influence
                High
                ↑
    ┌───────────┼───────────┐
    │ Keep       │ Manage    │
    │ Satisfied  │ Closely   │
    │            │           │
Low ├────────────┼───────────┤ High
Interest│ Monitor    │ Keep      │ Interest
    │            │ Informed  │
    └────────────┼───────────┘
                ↓
                Low

Response Strategies:
Manage Closely (High Power + High Interest): Core stakeholders
  → 1-on-1 deep interviews, regular reporting, decision participation, rapid response
Keep Satisfied (High Power + Low Interest): Potential threats
  → Regular briefings, milestone notifications, invite to key milestone meetings
Keep Informed (Low Power + High Interest): Potential allies
  → Regular newsletter, open meetings, feedback collection
Monitor (Low Power + Low Interest): Observe only
  → Announcement notification, no special management needed
```

##### Attitude-Influence Matrix

```
                Support Level
                ↑ Supportive
    ┌───────────┼───────────┐
    │ Champion   │ Ally      │
    │            │           │
Low ├────────────┼───────────┤ High
Influence│ Neutral    │ Blocker   │ Influence
    │            │           │
    └────────────┼───────────┘
                ↓
                ↓ Opposed

Conversion Strategies:
Blocker → Neutral: Understand concerns, provide security, demonstrate small wins
Neutral → Ally: Demonstrate value, invite participation, reduce risk perception
Ally → Champion: Empower + Recognize + Publicly thank
```

#### 6.3 Stakeholder Communication Plan

| Stakeholder | Role | Concerns | Communication Method | Frequency | Owner |
|-------------|------|----------|---------------------|-----------|-------|
| CEO | Final decision-maker | ROI / Strategic alignment / Risk | 1-on-1 briefing | Milestones | |
| CFO | Budget approver | Investment return / Cash flow impact | Financial analysis report | Monthly | |
| Business Leader | Requirements source | Efficiency gains / Cost reduction | Workshop + Weekly | Weekly | |
| Frontline User | End user | Is it easy to use? Will it increase workload? | Trial + Interview | Continuous | |
| IT Team | Implementer | Technical feasibility / Maintenance burden | Technical review | Weekly | |

#### Deliverables

1. **Stakeholder List & Matrix** (Power-Interest + Attitude-Influence)
2. **Stakeholder Communication Plan** (Who / What / How / How Often)
3. **Key Stakeholder Personas** (One page each: Concerns / Position / Influence strategy)

---

### Stage 7: Requirements Elicitation & Discovery

**Role: Requirements Analyst / Requirements Analyst**

> "80% of what users say are solutions, not requirements. The BA's core capability is extracting true requirements from solutions."

#### 7.1 Requirements Elicitation Technique Toolkit

| Technique | Description | Best For | Depth | Time Cost |
|-----------|-------------|----------|-------|-----------|
| **In-Depth Interview** | 1-on-1 structured/semi-structured | Mining deep needs, stakeholders | ⭐⭐⭐⭐⭐ | High |
| **Focus Group** | 6-10 person group discussion | Exploratory research, consensus building | ⭐⭐⭐ | Medium |
| **Observation** | Observe real user behavior on-site | Discover tacit needs users can't articulate | ⭐⭐⭐⭐⭐ | High |
| **Workshop** | Structured co-creation activity | Cross-department alignment, process mapping | ⭐⭐⭐⭐ | Medium-High |
| **Document Analysis** | Existing docs/systems/process analysis | Understanding current state (As-Is) | ⭐⭐⭐ | Medium |
| **Survey** | Large-scale quantitative collection | Hypothesis validation, quantifying needs | ⭐⭐ | Medium |
| **Prototyping** | Elicit feedback through prototypes | Ambiguous requirements, visual communication | ⭐⭐⭐⭐ | Medium-High |
| **Brainstorming** | Open-ended idea generation | Innovative solutions, breakthrough thinking | ⭐⭐⭐ | Low-Medium |

#### 7.2 In-Depth Interview Methodology

##### Interview Structure (SPIN Adapted + BA Enhanced)

```
Pre-Interview:
□ Research the interviewee (Background / KPIs / Pain points / Decision authority)
□ Prepare interview guide (Questions → Follow-up routes)
□ Confirm time / location / format (In-person > Remote, 1v1 > 1vMany)

In-Interview Three-Step Method (Context → Pain → Vision):
Stage 1: Establish Context (15%)
  "How do you currently do XX process?"
  "What roles/systems are involved?"

Stage 2: Deep Dive Pain Points (50%)
  "What are your top 3 pain points right now?"
  "How much does this problem impact your KPIs/personal goals?" (Quantify)
  "What solutions have you tried? Why didn't they work?"
  "If not resolved, what are the consequences?" (Amplify pain)

Stage 3: Paint the Vision (35%)
  "If you could change one thing, what would you most want to change?"
  "What does the ideal state look like?"
  "How much value would solving this create for you/your department?"

Key Techniques:
- 80% listen, 20% ask
- The power of silence: Pause 5 seconds, the other party will reveal more
- Ask "why" until root cause (5 Whys)
- Avoid leading questions ("Don't you think XX is bad?" → "What do you think of XX?")
- Distinguish between Observation (facts) and Judgment (interpretation)
```

##### Post-Interview Immediate Processing

```
Within 30 minutes after each interview:
1. Top 3 Key Findings
2. Surprising Discoveries (things you didn't know before)
3. Hypotheses to Validate
4. Contradictions with other interviews
5. Directions for next deep dive
```

#### 7.3 JTBD (Jobs-to-Be-Done) — BA Edition

```
B2B JTBD Framework:
┌─────────────────────────────────────────────────┐
│ When [a specific role in the organization]        │
│ I want to [complete a functional/emotional/social job] │
│ So that [achieve business outcome/KPI/compliance/risk mitigation] │
│                                                   │
│ Current approach: [How is it done now? Time/cost?] │
│ Pain level: [1-10, 10 = excruciating]             │
│ Frequency: [How often?]                            │
│ Constraints: [What limitations exist?]             │
│ Success criteria: [What counts as success?]        │
└─────────────────────────────────────────────────┘

B2B JTBD Examples:
Finance Manager: Complete consolidated statements for 3 subsidiaries within 3 days at month-end, meeting audit zero-defect standard
IT Admin: Batch-create 200 employee accounts + least-privilege assignment, meeting cybersecurity compliance
Procurement Manager: Compare 3 supplier quotes → pass approval → generate PO, compliance + efficiency
```

#### 7.4 Requirements Elicitation Common Pitfalls

| Pitfall | Manifestation | Avoidance |
|---------|--------------|-----------|
| **Premature Solution Focus** | User starts saying "I want XX feature" | Ask "What problem does this feature solve? How did you do it before?" |
| **Listening Only to the Loudest Voice** | Only focusing on the most vocal users | Include silent majority and high-value user perspectives |
| **Confirmation Bias** | Only hearing information that supports your preconceptions | Actively seek counter-evidence |
| **Users Don't Know What They Don't Know** | "I'm fine with how things are now" | Show possibilities, analogize from other industries |
| **Treating Features as Requirements** | "Need an Export to Excel feature" | "What's the purpose of exporting? What do you do after exporting?" |

#### Deliverables

1. **Interview Guide & Recording Template**
2. **JTBD Card Set** (organized by user role)
3. **Requirements Discovery Report** (TOP problems + Root causes + Quantified impact)
4. **Requirements Elicitation Plan** (Method / Target / Timing / Output)

---

### Stage 8: Requirements Analysis & Specification

**Role: Requirements Engineer / Requirements Engineer**

> "Well-written requirements are half the success; vague requirements are 100% of the failure."

#### 8.1 Requirements Classification System

```
Requirements Hierarchy Pyramid:
        ┌──────────┐
        │ Business  │ ← Why does the organization want to do this? (Business Requirements)
        │ Requirements│    Vision / Goals / Business Case
        │ (Why)     │
        ├──────────┤
        │ Stakeholder│ ← What does each role need? (Stakeholder Requirements)
        │ Requirements│    Role-perspective requirements
        ├──────────┤
        │ Solution  │ ← What should the solution do? (Solution Requirements)
        │ Requirements│
        │ ├Functional│    Functional: What the system must accomplish
        │ └Non-Func  │    Non-Functional: Performance / Security / Usability / Compliance
        ├──────────┤
        │ Transition│ ← What's needed to go from current to future state?
        │ Requirements│    Data migration / Training / Organizational change
        └──────────┘
```

#### 8.2 Requirements Documentation Standards

##### BRD (Business Requirements Document) Structure

```
1. Executive Summary
   - Problem/Opportunity statement (one sentence)
   - Proposed solution (one sentence)
   - Expected value (quantified)
   - Decision requested

2. Business Background & Problem
   - Current state (As-Is) description
   - Pain points and root cause analysis
   - Consequences of inaction

3. Vision & Objectives
   - Future state (To-Be) vision
   - SMART objectives
   - Success criteria and KPIs

4. Scope Definition
   - In scope / Out of scope
   - Constraints
   - Assumptions & Dependencies

5. Stakeholder Analysis
   - Roles & Needs
   - Decision authority & Influence

6. High-Level Requirements
   - Business requirements (Why)
   - Core functional requirements (What)
   - Non-functional requirements

7. Solution Analysis & Recommendation
   - Options evaluated (at least 3)
   - Recommended option with rationale
   - Cost-benefit analysis

8. Implementation Considerations
   - High-level timeline
   - Key milestones
   - Risks & Mitigation

9. Appendix
   - Detailed analysis data
   - Reference documents
```

##### User Story Standard

```
Standard Format (3C Principle):
As a [role]
I want to [function]
So that [value/purpose]

Acceptance Criteria:
Given [precondition]
When [action]
Then [expected result]

Good User Story INVEST Principle:
├── Independent (doesn't depend on other stories)
├── Negotiable (details can be discussed)
├── Valuable (valuable to user/business)
├── Estimable (team can estimate effort)
├── Small (granular, 1-3 days to complete)
└── Testable (clear acceptance criteria)
```

#### 8.3 Requirements Prioritization

##### MoSCoW Method

| Level | Meaning | Recommended % | Consequence of Not Delivering |
|-------|---------|--------------|------------------------------|
| **Must Have** | Must have, without it the project isn't complete | ≤60% | Solution unusable |
| **Should Have** | Should have, important but workaround exists | ~20% | Very inconvenient but usable |
| **Could Have** | Could have, nice to have | ~20% | Doesn't affect basic use |
| **Won't Have** | Won't do this release, into backlog | 0% this release | No impact |

##### KANO Model Application

```
Requirement Classification:
├── Must-Be: Missing → extreme dissatisfaction, Present → won't increase satisfaction
├── Performance: More is better, linear relationship
├── Delighters: Delight when present, OK when absent
├── Indifferent: No feeling either way → CUT!
└── Reverse: Actually reduces satisfaction → STOP IMMEDIATELY!

Survey Method:
Q1: If the train had WiFi, how would you feel?
Q2: If the train didn't have WiFi, how would you feel?
(Like / Expect / Neutral / Tolerate / Dislike)
→ Q1+Q2 answer combination → KANO classification
```

#### Deliverables

1. **BRD Business Requirements Document** (Full version / Summary version)
2. **User Story Map**
3. **Requirements Prioritization Table** (MoSCoW + KANO + Weighted Scoring)
4. **Requirements Traceability Matrix** (Business requirements → Functional requirements → Test cases)

---


### Stage 9: Solution Evaluation

**Role: Solution Analyst / Solution Analyst**

> "Evaluating solutions isn't about picking the cheapest — it's about choosing the one with the highest long-term business value."

#### 9.1 Solution Option Identification

```
Solution Option Expansion Thinking:
├── Buy: Purchase off-the-shelf product/service
├── Build: Internal development
├── Hybrid (Buy+Build): Core self-built + peripheral purchased
├── Outsource: Outsource to third party
├── Partner: Collaborate with partners
├── Process Change: Don't change the system, change the process
├── Do Nothing: Maintain status quo ← ALWAYS include as an option!
└── Combination: Multiple of the above

Note: Do Nothing is the most underrated option
→ Provides a quantified baseline, making other options' value clearer
→ Sometimes Do Nothing is indeed the best choice (when ROI doesn't exist)
```

#### 9.2 Solution Evaluation Methods

##### Weighted Scoring Method

| Evaluation Dimension | Weight | Option A | Option B | Option C | Do Nothing |
|---------------------|--------|----------|----------|----------|------------|
| Business Value Realization | 25% | 4(1.0) | 3(0.75) | 5(1.25) | 1(0.25) |
| Total Cost of Ownership (TCO) | 20% | 3(0.6) | 4(0.8) | 2(0.4) | 5(1.0) |
| Implementation Risk | 15% | 3(0.45) | 4(0.6) | 2(0.3) | 5(0.75) |
| Implementation Speed | 15% | 2(0.3) | 3(0.45) | 4(0.6) | 5(0.75) |
| Strategic Alignment | 10% | 5(0.5) | 4(0.4) | 3(0.3) | 1(0.1) |
| Scalability | 10% | 4(0.4) | 3(0.3) | 5(0.5) | 1(0.1) |
| Organizational Fit | 5% | 3(0.15) | 4(0.2) | 3(0.15) | 5(0.25) |
| **Total Score** | | **3.40** | **3.50** | **3.50** | **3.20** |

##### TCO Analysis (Total Cost of Ownership)

```
TCO = One-Time Costs + Ongoing Operating Costs (N years)

One-Time Costs:
├── Software license / Purchase fee
├── Hardware / Infrastructure
├── Implementation / Integration services
├── Data migration
├── Custom development
└── Training

Ongoing Costs (Annual):
├── License renewal / Subscription
├── Operations / Support
├── Labor costs (FTEs maintaining this system)
├── Upgrades / Updates
├── Infrastructure / Cloud services
└── Opportunity cost (other opportunities forgone by choosing this option)

3-Year TCO Comparison:
Option A: $2M + 3×$0.5M = $3.5M
Option B: $0.5M + 3×$1M = $3.5M  ← Same TCO, different cash flow
Option C: $5M + 3×$0.2M = $5.6M
```

#### 9.3 Make vs. Buy Analysis

```
Make (Build) Signals:
□ This is a core differentiating capability → Can't use standard products
□ No suitable product exists in the market
□ Deep customization needed, purchase + modification cost > build cost
□ Maintenance costs controllable, capability to maintain long-term
□ Purchasing would create vendor lock-in risk

Buy Signals:
□ This is infrastructure/common capability → Self-build creates no competitive advantage
□ Mature SaaS products exist in the market
□ The organization lacks the skills/resources needed for self-build
□ Need rapid go-live (purchase much faster than self-build)
□ Supplier ecosystem is mature, no lock-in risk

Hybrid Strategy:
□ Core differentiating → Self-build
□ Non-core/Common → Purchase
□ Customization needs → Purchase + secondary development (evaluate long-term maintenance cost)
```

#### Deliverables

1. **Solution Options Analysis Report** (3+ options, with weighted scoring + TCO comparison)
2. **Make vs. Buy Recommendation** (with long-term cost/risk assessment)
3. **Recommended Solution Summary** (Decision-maker version, one-pager)

---

### Stage 10: Business Case & Investment Decision

**Role: Business Case Specialist / Business Case Specialist**

> "A business case isn't a PPT beauty contest — it's using numbers and logic to make it impossible for decision-makers to say no."

#### 10.1 Business Case Five-Element Model

```
┌─────────────────────────────────────────────┐
│ 1. Strategic Alignment                       │
│    → How does this investment support company strategy? │
│    → Relationship to company OKRs/strategic goals │
├─────────────────────────────────────────────┤
│ 2. Economic Value                            │
│    → Financial returns: NPV/IRR/ROI/Payback │
│    → Non-financial value: Risk reduction/Compliance/Strategic options │
├─────────────────────────────────────────────┤
│ 3. Commercial Viability                      │
│    → Does the market exist? Will customers buy? │
│    → Is competitive advantage sustainable?   │
├─────────────────────────────────────────────┤
│ 4. Organizational Capability                 │
│    → Can we deliver?                         │
│    → What capabilities/resources are needed? Gaps? │
├─────────────────────────────────────────────┤
│ 5. Risk & Mitigation                         │
│    → What are the key risks?                 │
│    → If the worst case happens, can we absorb it? │
└─────────────────────────────────────────────┘
```

#### 10.2 Investment Return Analysis

##### Cost-Benefit Analysis

```
Benefit Categories:
├── Directly Quantifiable Benefits ✓
│   ├── Incremental Revenue: New products / New markets / Price increases
│   ├── Cost Savings: Labor / Materials / Operations
│   └── Efficiency Gains: Time saved × Labor cost
│
├── Indirectly Quantifiable Benefits (Medium Confidence)
│   ├── Risk Reduction Value: Risk probability × Loss amount × Reduction %
│   ├── Customer Retention Improvement: Reduced churn × Customer value
│   └── Employee Efficiency: Saved FTEs × Average salary
│
└── Qualitative Benefits (must explain logic and confidence)
    ├── Strategic option value
    ├── Brand / Reputation enhancement
    └── Compliance / Regulatory risk avoidance

Cost Categories:
├── Certain Costs:
│   ├── Software / Hardware procurement
│   ├── Implementation / Integration / Consulting fees
│   └── Data migration
│
├── Estimated Costs (±20%):
│   ├── Internal labor investment
│   ├── Training / Change management
│   └── Operations & Maintenance
│
└── Uncertain Costs (±50%):
    ├── Scope creep
    ├── Integration complexity
    └── Learning curve
```

##### Sensitivity Analysis

```
Key Assumptions:
├── Revenue growth assumption (most uncertain factor)
├── Cost savings assumption (second most uncertain)
├── Implementation timeline assumption
└── Discount rate assumption

Sensitivity Test:
│ Scenario      │ Revenue Growth │ NPV    │ IRR  │
│ Optimistic    │ +20%           │ $5M    │ 35%  │
│ Base Case     │ 10%            │ $2M    │ 22%  │
│ Pessimistic   │ 0%             │ -$1M   │ 5%   │ ← Can we absorb this?

Key Question: Under what conditions would this investment fail?
→ Find the "fatal assumption" and prioritize validation
```

#### 10.3 Business Case Document Structure

```
1. Executive Summary
   - 1 paragraph: Problem + Solution + Value + Request
   - Key numbers: Investment / NPV / IRR / Payback period

2. Problem & Opportunity
   - Current state (As-Is) and pain points
   - Opportunity size (quantified)
   - Cost of inaction

3. Proposed Solution
   - Solution description (What + How)
   - Link to strategy
   - Why this is the best choice

4. Financial Analysis
   - Investment overview (Initial + Ongoing costs)
   - ROI / NPV / IRR / Payback
   - Sensitivity analysis
   - Non-financial benefits

5. Risk Analysis
   - Top 5 key risks
   - Mitigation strategies
   - If the worst case happens

6. Implementation Roadmap
   - Key milestones
   - Resource requirements
   - Dependencies & Prerequisites

7. Recommendation & Decision Request
   - Clear decision request
   - Consequences if not approved
```

#### Deliverables

1. **Business Case Document** (Full version + Decision summary version)
2. **Financial Model** (Excel, with NPV/IRR/Sensitivity analysis)
3. **Investment Decision PPT** (Board-level, 10 pages or fewer)

---

### Stage 11: Business Process Analysis & Reengineering

**Role: Process Analyst / Process Analyst**

> "Processes are the DNA of organizational capability. Changing processes is harder than changing systems, but the payoff is also greater."

#### 11.1 Process Modeling Standard (BPMN 2.0)

```
BPMN Core Elements:

Events:
├── Start Event ○ → Process start
├── Intermediate Event ◎ → Things happening during the process
└── End Event ◎ → Process end

Activities:
├── Task □ → Atomic unit of work
└── Sub-Process □+ → Expandable composite activity

Gateways:
├── Exclusive Gateway ◇× → Only one path
├── Parallel Gateway ◇+ → All paths simultaneously
└── Inclusive Gateway ◇○ → One or more paths

Flows:
├── Sequence Flow → → Activity order
└── Message Flow ⇢ → Messages across participants/organizations

Swimlanes:
├── Pool □ → Organizational boundary
└── Lane ─ → Role division
```

#### 11.2 Process Analysis Toolkit

##### SIPOC Analysis (High-Level Process)

```
SIPOC = Supplier → Input → Process → Output → Customer

Example: Procurement Approval Process
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ Supplier │  Input   │ Process  │  Output  │ Customer │
├──────────┼──────────┼──────────┼──────────┼──────────┤
│Requesting │Purchase  │Submit→   │Approval  │Requesting │
│Dept      │Request   │Approve   │Decision  │Dept      │
│Procurement│Supplier  │→Compare→ │Purchase  │Finance   │
│Dept      │Quotes    │→Contract │Order     │Dept      │
│Supplier  │Contract  │→Sign→    │Contract  │Supplier  │
│          │          │→Receive  │Receipt   │Warehouse │
└──────────┴──────────┴──────────┴──────────┴──────────┘

SIPOC Advantage: Drawn in 5 minutes, rapid high-level alignment
```

##### Value Stream Mapping (VSM)

```
Value Stream Map Elements:
├── Process Box: Each process step
├── Data Box: Time / Quality / Wait time metrics
├── Information Flow: How information is transmitted (arrows)
├── Timeline:
│   ├── Value-Added Time: Actual working time
│   ├── Non-Value-Added Time: Waiting / Moving / Rework
│   └── Efficiency = VAT / Total Lead Time

Typical B2B process efficiency <10% (90% of time spent waiting and handoffs!)

Improvement Directions:
├── Eliminate: Which steps are completely unnecessary?
├── Simplify: Which steps can be simpler?
├── Integrate: Which steps can be combined?
├── Automate: Which steps can the system do automatically?
└── Parallelize: Which steps can happen simultaneously?
```

##### Process Maturity Model

```
Level 1: Initial — No fixed process, varies by person
Level 2: Managed — Process documented, basically consistent execution
Level 3: Standardized — Process standardized, KPI monitoring
Level 4: Predictable — Process quantitatively managed, predictable
Level 5: Optimizing — Process continuously optimized, automation + AI

Most enterprises are at Level 2-3
Level 2 → Level 3 is the biggest leap (standardization brings manageability)
```

#### 11.3 Business Process Reengineering (BPR) Methodology

##### Hammer & Champy BPR 7 Principles

```
1. Organize around outcomes, not tasks
   ❌ Each person does one step → ✅ One person/team responsible for complete outcome

2. Let those who use the output perform the process
   ❌ Procurement is Procurement Dept's job → ✅ Departments that need procurement do it themselves (within rules)

3. Integrate information processing into the work that produces the information
   ❌ Data entry is one group, analysis is another → ✅ Source entry, system analysis

4. Treat geographically dispersed resources as centralized (use IT for virtual centralization)
   ❌ Each department has its own HR/budget → ✅ Shared resource pool, on-demand allocation

5. Link parallel activities instead of just integrating results
   ❌ Departments work in parallel → assemble at the end → ✅ Continuous communication, integrate during the process

6. Put decision points where work is performed, build control into the process
   ❌ Operator → Supervisor → Manager step-by-step approval → ✅ Autonomy within rules, escalate only exceptions

7. Capture information once at the source
   ❌ Re-enter at every step → ✅ Enter once, share throughout
```

#### Deliverables

1. **As-Is Process Model** (BPMN 2.0)
2. **Process Pain Point Analysis Report** (with quantification: time / error rate / cost)
3. **To-Be Process Design** (with improvement plan + expected benefits)
4. **Value Stream Map** (with value-added / non-value-added analysis)

---

### Stage 12: Data Analysis & Business Intelligence

**Role: Data BA / Analytics BA**

> "Business analysis without data support is just guessing. But data doesn't speak for itself — it needs human interpretation."

#### 12.1 Data Analysis Hierarchy Model

```
Value
 ↑
 │  ┌─────────────────────────┐
 │  │ Prescriptive Analytics    │ ← Machine Learning / AI
 │  │ (What will happen?)      │    Churn prediction, Demand forecasting
 │  ├─────────────────────────┤
 │  │ Predictive Analytics      │ ← Optimization / Simulation
 │  │ (What should we do?)     │    Optimal pricing, Inventory optimization
High│  ├─────────────────────────┤
 │  │ Diagnostic Analytics      │ ← Root Cause Analysis
 │  │ (Why did it happen?)     │    Why did sales drop?
 │  ├─────────────────────────┤
 │  │ Descriptive Analytics     │ ← BI Dashboards
 │  │ (What happened?)         │    Daily/Weekly/Monthly reports
Low│  └─────────────────────────┘
 └────────────────────────────────→ Difficulty / Cost
```

#### 12.2 Business Performance Analysis Framework

##### Revenue Analysis Framework

```
Revenue = Customers × Average Order Value × Purchase Frequency

Customer Breakdown:
├── New Customers = Traffic × Conversion Rate
├── Retained Customers = Previous Period Customers × (1 - Churn Rate)
└── Returning Customers = Churned Customers × Recall Rate

Average Order Value Breakdown:
├── Unit Price = Σ(Product Unit Price × Sales Volume Share)
├── Attachment Rate = Products per Order
└── Discount Rate = Actual Transaction Price / List Price

Purchase Frequency:
├── Repurchase Cycle = Interval between first and second purchase
└── Customer Lifetime = Time span from first to last purchase
```

##### Profit Analysis Framework

```
Profit = Revenue - Variable Costs - Fixed Costs

Contribution Margin = Revenue - Variable Costs
→ Incremental profit per additional unit sold
→ Assessment: Which products/customers have the highest contribution margin?

Break-Even Point = Fixed Costs / (1 - Variable Cost Ratio)
→ How much revenue is needed to cover costs?
→ Margin of Safety = (Actual Revenue - Break-Even Point) / Actual Revenue

Operating Leverage = Contribution Margin / Net Profit
→ For every 1% revenue growth, how much % profit growth?
→ Asset-heavy companies have high operating leverage (high fixed costs)
```

#### 12.3 KPI System Design

##### North Star Metric Selection

```
Good North Star Metric Characteristics:
├── Reflects real value to customers (not vanity metrics)
├── Correlates with long-term business outcomes
├── Simple and actionable for improvement
├── Measurable and timely
└── Guides teams to make correct decisions

Common North Star Metrics:
├── SaaS: WAU (Weekly Active Users) / NRR (Net Revenue Retention) / Quick Ratio
├── E-commerce: GMV / Repurchase Rate / AOV
├── Platform: Transactions / Match Success Rate
├── Finance: AUM (Assets Under Management) / NPL Ratio
└── Media: DAU / User Time Spent / Ad Fill Rate
```

##### OKR & KPI Design

```
OKR = Objectives + Key Results
├── OKR focuses on "what to change" — direction and ambition
├── KPI focuses on "current state" — steady-state metrics
├── OKR drives transformation, KPI maintains order
└── Good organizations run OKR and KPI in parallel

KPI Design SMART:
├── Specific: What exactly does it refer to?
├── Measurable: Can be quantified
├── Achievable: Attainable but requires effort
├── Relevant: Connected to strategy
└── Time-bound: Clear time limit
```

#### Deliverables

1. **Business Performance Analysis Report** (Monthly/Quarterly, with revenue breakdown + profit analysis)
2. **KPI System Design** (North Star Metric + OKR + KPI Tree)
3. **BI Dashboard Requirements** (Core dashboards + Drill-down paths + Alert rules)
4. **Data Quality Assessment** (Completeness / Accuracy / Timeliness / Consistency)

---


### Stage 13: Risk Analysis & Decision Science

**Role: Risk Analyst / Risk Analyst**

> "The essence of risk management isn't eliminating risk — it's making the cost of risk bearable."

#### 13.1 Risk Identification Framework

##### Risk Classification System

```
Strategic Risks:
├── Market Risk (demand changes / new entrants / substitutes)
├── Technology Risk (wrong tech choice / disruption / tech debt)
├── Business Model Risk (unit economics don't work / unsustainable burn)
├── Competitive Risk (price wars / competitor innovation / market erosion)
└── Reputation Risk (trust crisis / public opinion incidents / compliance scandals)

Operational Risks:
├── Process Risk (process breakdown / inefficiency / quality fluctuations)
├── People Risk (key person departure / capability gaps / culture conflict)
├── Supplier Risk (supply disruption / price increases / quality decline)
├── System Risk (downtime / security breaches / data loss)
└── Compliance Risk (regulatory violations / contract breaches / IP)

Financial Risks:
├── Liquidity Risk (cash flow disruption / financing failure)
├── Credit Risk (customer non-payment / bad debt)
├── FX/Interest Rate Risk
└── Valuation Risk (down rounds / goodwill impairment)

External Risks:
├── Macro Risk (economic recession / inflation / geopolitical)
├── Regulatory Risk (new regulations / policy changes / trade sanctions)
├── Natural Risk (pandemic / natural disasters / climate risk)
└── Social Risk (public opinion / social movements / demographic changes)
```

##### Risk Identification Methods

| Method | Description | Best For |
|--------|-------------|----------|
| **Expert Interview** | In-depth interviews with key stakeholders | All stages |
| **Brainstorming** | Team co-creation to identify risks | Early stage |
| **Checklist** | Based on historical project risk lists | Standardization |
| **Assumption Analysis** | Overturn each key assumption | Strategy stage |
| **SWOT** | Weaknesses (W) + Threats (T) = Risks | General |
| **FMEA** | Failure Mode and Effects Analysis | Process/Product |
| **Scenario Planning** | Multiple future scenario exploration | Major decisions |

#### 13.2 Risk Assessment

##### Risk Scoring Matrix

```
Risk Score = Likelihood (1-5) × Impact (1-5)

Likelihood:
1 = Almost impossible (<5%)  2 = Unlikely (5-20%)  3 = Possible (20-50%)
4 = Likely (50-80%)          5 = Almost certain (>80%)

Impact:
1 = Negligible  2 = Minor  3 = Moderate (affects goal achievement)
4 = Severe (affects multiple goals)  5 = Catastrophic (threatens organizational survival)

Risk Heat Map:
Impact ↑
  5  │   M    H    H    C    C
  4  │   M    M    H    H    C
  3  │   L    M    M    H    H
  2  │   L    L    M    M    M
  1  │   L    L    L    L    M
     └─────────────────────────→ Likelihood
        1    2    3    4    5

C=Critical (Act immediately) H=High (This week) M=Medium (This month) L=Low (Monitor)
```

##### FMEA (Failure Mode and Effects Analysis)

```
RPN (Risk Priority Number) = Severity(S) × Occurrence(O) × Detection(D)

Each 1-10:
Severity: If it happens, how big is the impact?
Occurrence: How likely is it to happen?
Detection: Can it be detected before happening? (10 = undetectable)

RPN > 100 → Must act
RPN 50-100 → Recommended action
RPN < 50 → Acceptable

Response Strategies:
├── Reduce Severity → Modify design / Add buffers
├── Reduce Occurrence → Preventive measures / Standardization
└── Improve Detection → Early warning / Monitoring systems
```

#### 13.3 Decision Analysis

##### Decision Tree

```
Decision Tree Elements:
□ Decision Node → Your choice
○ Chance Node → Uncertain outcome
△ Terminal Node → Final outcome value

Example: New Product Investment Decision
         ┌── Success (60%) → +$5M
Invest $1M─┤
         └── Failure (40%) → -$1M
EMV (Expected Monetary Value) = 60%×$5M + 40%×(-$1M) - $1M = $1.6M

Decision Tree Value:
- Makes uncertainty explicit
- Quantifies the value of complex decisions
- Identifies "value of information" (how much is more research worth?)
```

##### Multi-Criteria Decision (AHP — Analytic Hierarchy Process)

```
Pairwise Comparison Matrix (1-9 Scale):
1=Equal importance  3=Slightly more important  5=Significantly more important
7=Very strongly more important  9=Extremely more important

     Cost  Quality  Speed  Weight
Cost  1     1/5      1/3    11%
Quality 5    1        3      63%  ← Quality is most important
Speed  3    1/3      1      26%

Consistency Check: CR < 0.1 (judgment logic is consistent)

Best for: When decisions involve multiple dimensions that can't be directly compared
Widely used in: Supplier selection, project ranking, strategic prioritization
```

#### Deliverables

1. **Risk Register** (with 100+ risk items + scoring + response strategies)
2. **FMEA Analysis Table** (with RPN + improvement priorities)
3. **Decision Analysis Document** (Decision Tree / AHP / Multi-criteria scoring)
4. **Risk Monitoring Dashboard** (Key risk indicators + alert thresholds)

---

### Stage 14: Implementation & Change Management

**Role: Change Management BA / Change BA**

> "The best analysis, if it can't be implemented, is not only worthless — it also consumes trust."

#### 14.1 Implementation Planning

##### Implementation Roadmap

```
Phase 0: Preparation (4-8 weeks)
├── Project team formation
├── Detailed plan development
├── Vendor/Partner selection
└── Environment/Infrastructure setup

Phase 1: Pilot/PoC (4-12 weeks)
├── Select representative small-scale pilot
├── Rapidly validate key assumptions
├── Collect feedback and adjust solution
└── Build internal success stories

Phase 2: Rollout (8-24 weeks)
├── Batch rollout by department/region
├── Legacy system parallel run
├── Data migration + validation
└── User training + support

Phase 3: Stabilization & Optimization (Ongoing)
├── Legacy system decommission/archive
├── Continuous feedback collection and optimization
├── KPI achievement check
└── Lessons learned → Standardization
```

##### Implementation Risk Assessment

```
Top 5 Reasons for Implementation Failure:
1. Requirements misunderstood (built the wrong thing from the start)
2. User resistance (nobody uses it)
3. Data quality issues (data found unreliable after migration)
4. Scope creep (endless feature additions, never finished)
5. Insufficient leadership support (abandoned when difficulties arise)

Response:
1→ Frequent prototype validation | 2→ Change management | 3→ Early data audit
4→ Strict change control | 5→ Regular reporting to sponsor
```

#### 14.2 Change Management

##### Kotter's 8-Step Change Model

```
Step 1: Create Urgency
  → Show the cost and consequences of not changing
  → Use data AND stories to create urgency (data alone isn't enough)

Step 2: Build a Guiding Coalition
  → Find a change coalition with influence + authority + commitment
  → At least 3-5 key people

Step 3: Form a Strategic Vision
  → Vision: Why are we changing? What will it look like after?
  → Can explain the vision in 30 seconds

Step 4: Communicate the Change Vision
  → Multi-channel repeated communication
  → Leaders walk the talk (the most important communication method)

Step 5: Empower Employees to Act
  → Remove obstacles (systems/processes/people)
  → Encourage risk-taking and non-traditional ideas

Step 6: Generate Short-Term Wins
  → Must have a visible win within the first 30 days
  → Publicize and celebrate this win

Step 7: Consolidate Gains and Drive More Change
  → Use the trust from short-term wins to push bigger changes
  → Don't declare "victory" too early (change takes 2-3 years)

Step 8: Anchor Changes in the Culture
  → Make the new way "the way we do things around here"
  → Connect the change to organizational success
```

##### Change Curve Management

```
Y-axis: Morale / Productivity
    ↑
    │     ┌────────────────────
    │    /  ← Acceptance & Exploration    ↑
    │   /                                 New Normal
    │  /  ← Experimentation & Learning
    │ /
    │/    ← Resistance & Denial
    │     ← Shock & Denial
    └──────────────────────→ X-axis: Time

BA Strategy by Stage:
Shock: Listen + Understand feelings + Don't push too fast
Resistance: Understand concerns + Provide information + Show small examples
Exploration: Training + Support + Encourage experimentation
Acceptance: Standardize + Reward + Anchor
```

#### Deliverables

1. **Implementation Roadmap** (with phases / milestones / resources / dependencies)
2. **Change Management Plan** (with communication / training / support / risks)
3. **Go-Live Checklist** (must-check items before launch)
4. **Post-Implementation Review Report** (Actual vs. Planned / Lessons learned)


---
