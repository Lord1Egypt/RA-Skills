# B2B Product Manager Common Methodologies — In-Depth Handbook

## 1. B2B-Specific Product Evaluation Frameworks

### 1.1 B2B Product Health Assessment Model

```
Product Health = Customer Health × 0.4 + Business Health × 0.3 + Product Health × 0.3

Customer Health:
├── NRR (Net Revenue Retention) > 100%
├── NPS > 30
├── Logo Churn < 5% (annualized)
├── Core Feature Adoption Rate > 60%
└── CES (Customer Effort Score) < 3 (1–7 scale)

Business Health:
├── ARR Growth Rate > 30%
├── LTV/CAC > 3
├── Gross Margin > 70%
├── CAC Payback < 18 months
└── Expansion MRR Share > 20%

Product Health:
├── Core Feature Availability > 99.9%
├── P0 Bug Fix < 24h
├── Feature Delivery Cycle < 4 weeks
└── Requirement Throughput MoM Growth > 10%
```

### 1.2 B2B Product Lifecycle Stage Identification

| Stage | Characteristics | Core Task | North Star Metric Example |
|------|------|---------|--------------|
| **0→1 PMF Exploration** | < 10 customers | Find PMF, survive | Number of willing paying customers |
| **1→10 PMF Verification** | 10–50 customers | Verify replicability | NRR > 100%, NPS > 30 |
| **10→100 Efficiency Expansion** | 50–200 customers | Standardization + Efficiency | ARR growth rate, CAC optimization |
| **100→N Scale** | > 200 customers | Ecosystem + Platform-based | Market share, platform GMV |

---

## 2. B2B-Specific Methodologies

### 2.1 Permission Model Design Methodology

#### RBAC (Role-Based Access Control)

```
Design Steps:
1. Enumerate all operations (pages / buttons / APIs / data scopes)
2. Define roles (based on organizational structure)
3. Role–operation mapping (permission matrix)
4. User–role binding
5. Data permission policy overlay (row-level / column-level)

B2B Permission Check Flow:
User requests resource → Get user role list → Get role permission list
→ Check resource permission → Check data permission → Allow / Deny
```

#### ABAC (Attribute-Based Access Control)

Applicable scenarios: when role-based permissions are not granular enough and attribute-dimension control is needed.

```
Example Policy:
"Allow department managers to edit leave applications submitted by
employees in their own department during working hours 9:00–18:00 on weekdays"

Attribute Dimensions:
- Subject attributes: role, department, job level, hire date
- Resource attributes: type, status, owning department, classification level
- Environment attributes: time, IP address, device type
- Action attributes: read / write / delete / approve / export
```

### 2.2 Approval Workflow Design Methodology

#### Approval Workflow Design Decision Tree

```
Is approval required?
├── Yes → Approval workflow type?
│   ├── Fixed workflow (fixed roles) → e.g., expense approval (employee → manager → finance → cashier)
│   ├── Dynamic workflow (conditional branching) → e.g., amount < 5000 manager approval, > 5000 add finance approval
│   ├── Countersign (unanimous approval) → e.g., major contracts, all VPs must agree
│   ├── Or-sign (any one approval) → e.g., duty approval, any admin can approve
│   └── Escalation approval → e.g., escalate step by step along org hierarchy
└── No → Execute operation directly
```

#### Approval Efficiency Design Principles

```
1. Approval nodes ≤ 5 (must justify necessity if exceeding 5)
2. Approvers per node ≤ 3
3. Timeout auto-policy (reminder / escalation / auto-approve / auto-reject)
4. Mobile approval must be supported
5. Approval detail page must include: full information + approval history + action buttons
6. Support batch approval (one-click approve for same-type requests)
7. Approver view: pending approval list + approved list
8. Requester view: my applications + approval progress
```

### 2.3 Multi-Tenant Architecture Design Methodology

```
Tenant Isolation Decision Matrix:

Evaluation Dimension        → Determines Isolation Level
├── Customer compliance reqs → High → Independent Deployment
├── Data sensitivity         → High → Independent Database
├── Customer customization   → High → Independent Schema
├── Customer count           → High → Shared Table
├── Ops capability           → Low → Shared Table
└── Cost tolerance           → Low → Shared Table

Recommended Strategy:
- Early stage: Row-Level (tenant_id), quick go-live
- Reserve: Schema-Level interface, prepared for key accounts
- Ultimate: Database-Level automated deployment capability
```

### 2.4 B2B Data Dictionary Design

```
Data Dictionary Layers:
L1 Base Fields: ID, created_by, created_at, updated_by, updated_at, tenant_id, version
L2 Business Fields: regular fields defined per business requirements
L3 System Fields: status, process_instance_id, approval_status
L4 Extension Fields: tenant-level customizable fields (EAV model or JSON columns)

Field Naming Conventions:
- Boolean: is_xxx / has_xxx
- Timestamp: xxx_at (created_at, updated_at, deleted_at, approved_at)
- Monetary: xxx_amount (unit: cents, use DECIMAL to avoid precision issues)
- Enum: xxx_type / xxx_status
- Foreign key: xxx_id
- Count: xxx_count / xxx_num
```

### 2.5 B2B Integration Patterns

```
Enterprise Integration Maturity Model:
L1: File import/export (CSV / Excel)
L2: Webhook + message notifications
L3: RESTful API
L4: SSO + org structure sync
L5: Deep integration (bidirectional data sync + embedded components)

Adoption Recommendations by Stage:
- MVP stage: at least reach L1 (import/export)
- GTM stage: at least reach L3 (API + Webhook)
- Scale stage: at least reach L4 (SSO + org sync)
```

### 2.6 B2B Pricing Strategy Methodology (V1.1.0 Deep Upgrade)

#### Two Dimensions of SaaS Pricing

```
Dimension 1: Usage (Usage-Based)
├── Per API call
├── Per storage space (GB)
├── Per compute resource (CPU/GPU hours)
├── Per message/event count
├── Per data analysis volume
└── Per active user (MAU)

Dimension 2: Feature Complexity (Feature-Based)
├── Basic Plan: core features, anchor the low end
├── Professional Plan: flagship package, highest gross margin
├── Enterprise Plan: key-account customization, contact sales
└── Hybrid Plan: base fee + usage fee (balancing predictability and flexibility)
```

#### The 10 SaaS Pricing Models — Full Landscape

| # | Pricing Model | Billing Unit | Applicable Scenarios | Representative Products | 2026 Trend |
|---|---------|---------|---------|---------|---------|
| 1 | **Flat Rate** | Fixed monthly/annual | Simple features, stable user count | Basecamp | Declining share |
| 2 | **Per User** | Per user/month | Collaboration tools, CRM | Salesforce, Slack | Still mainstream |
| 3 | **Tiered Pricing** | Tiered by feature package | SaaS mainstream | HubSpot, Zoom | **67% of companies adopt** |
| 4 | **Usage-Based** | API calls / GB / events | Infrastructure, AI APIs | AWS, OpenAI | **Fastest growing** |
| 5 | **Feature-Based** | Per feature module | Complex enterprise software | ERP, HR systems | Stable |
| 6 | **Hybrid Pricing** | Base fee + usage | Balancing predictability and flexibility | Twilio, Stripe | **38% include usage element** |
| 7 | **Per Storage** | Per GB/month | Cloud storage, data platforms | Dropbox, Snowflake | Mature |
| 8 | **Per Transaction** | % per transaction | Payments, e-commerce platforms | Stripe, Shopify | Stable |
| 9 | **Per Active User** | Monthly active users | Communities, collaboration platforms | Slack (partial) | Growing |
| 10 | **Value-Based** | % of value created | AI efficiency gains, ROI tools | Emerging model | Frontier exploration |

#### 2026 Market Trend Data

| Metric | Data | Source |
|------|------|------|
| Tiered pricing adoption rate | 67% | Profitwell |
| Pure usage-based adoption rate | 18% | Profitwell |
| Hybrid pricing with usage element | 38% | Profitwell |
| Projected preference for usage-based by 2026 | 70% | Gartner |
| Hybrid pricing enterprise renewal rate | 12% higher than pure tiered | OpenView |

#### Seven-Step Pricing Implementation Process

```
Step 1: Value Quantification
  - How much time saved for the customer? (convert to labor cost)
  - How much risk avoided for the customer? (convert to loss cost)
  - How much revenue created for the customer? (incremental revenue)
  - Price after quantification is typically 1/3 ~ 1/10 of quantified value

Step 2: Pricing Dimension Selection
  - Per user? (collaboration products)
  - Per feature? (large feature differentiation)
  - Per usage? (API / storage / compute)
  - Per outcome? (GMV commission / performance-based)
  - Hybrid? (base fee + usage)

Step 3: Plan Design
  - Basic Plan: anchor the low end, get customers in the door
  - Professional Plan: flagship package, highest gross margin
  - Enterprise Plan: leave for key-account negotiation
  - Golden Rule: 3 plans, the middle one is the recommendation

Step 4: Pricing Numbers
  - Psychological pricing: ¥999 > ¥1000 (perceived difference of 100)
  - Annual discount: monthly × 10 ≈ annual price (≈ 17% off)
  - Tiered pricing: the more users, the lower the unit price

Step 5: Pricing Page Design
  - Highlight recommended plan ("Most Popular" badge)
  - Feature comparison table (✓ / ✗)
  - FAQ section (address pricing concerns)
  - Contact sales entry (Enterprise plan)

Step 6: Discount Rule Management
  - Unmanaged discounts erode 200–400 bps of gross margin annually
  - Discount rules: automation + approval workflow + margin visibility
  - Annual 20% off, volume tiered discounts, competitive discounts (requires approval)

Step 7: Pricing Monitoring & Iteration
  - Track per-plan conversion rates, ARPU changes
  - PSM price sensitivity testing (PMC / PME / OPP / IPP)
  - 1% pricing improvement = 8.7% profit increase (McKinsey data)
```

#### Pricing Challenges in the AI Era

| Challenge | Description | Response Strategy |
|------|------|---------|
| **Token Pricing** | Inference costs continue to drop; fixed token prices may lose competitiveness | Dynamic pricing or "outcome-based pricing" |
| **Inference Cost Volatility** | Costs vary significantly across models and time windows | Cost-plus-premium model rather than fixed unit price |
| **Agent Call Chains** | A single user request may trigger multiple model calls | Bill by "task completion" rather than "token count" |

### 2.7 PLG (Product-Led Growth) Methodology (V1.1.0 New)

#### PLG Core Funnel

```
Acquisition → Activation → Retention → Revenue → Referral

Key Metrics:
- PQL (Product Qualified Leads): leads qualified through product usage behavior indicating purchase intent
- Time-to-Value (TTV): time from signup to experiencing core value
- PQL Conversion Rate: PQL → SQL → Closed Won
```

#### PLG China Market Adaptation Analysis

| Dimension | Overseas PLG | China PLG Adaptation |
|------|--------|-----------|
| Self-Serve Signup | Credit card self-serve | Must support WeChat Pay / Alipay + invoicing |
| Free Trial | 14–30 days | Recommend 30–60 days (longer decision chain) |
| Decision Model | Individual / small team trial → evangelize | Must cover both decision-maker and end-user tracks |
| Paid Conversion | Online self-serve upgrade | Often requires sales involvement (PLS model) |

#### Product-Led Sales (PLS) Hybrid Model

```
PLG (Product-Led)                   SLG (Sales-Led)
     │                                    │
     ├── Self-serve signup/trial          ├── Key-account customization
     ├── In-product upgrade guidance      ├── Contract negotiation
     └── Self-serve payment               └── Invoicing / procurement process
                  │
                  ▼
          PLS (Product-Led Sales)
     ┌─────────────────────────────────────────┐
     │ Use product usage data to identify      │
     │ sales signals                           │
     │ Sales intervene at critical moments     │
     │ 65% of buyers prefer hybrid experience  │
     └─────────────────────────────────────────┘
```

#### PQA (Product Qualified Account) Scoring Model

| Dimension | Weight | Signal Examples |
|------|------|---------|
| Product Usage Depth | 30% | Core feature usage frequency, advanced feature activation |
| Team Size | 20% | Team headcount, number of departments |
| Usage Growth | 20% | MoM usage growth, new feature adoption speed |
| Company Profile | 15% | Industry, size, tech stack |
| Intent Signals | 15% | Pricing page visits, upgrade button clicks, support inquiries |

> **McKinsey Key Finding**: Only a few PLG companies achieve outstanding performance; PLS is the key differentiator. The pure-PLG trap: self-serve model struggles to cover complex key-account needs. The core of PLS: use product data to drive sales, not replace sales.

### 2.8 JTBD (Jobs-to-Be-Done) Methodology (V1.1.0 New)

#### Core Principle

Users "hire" a product to complete a job, not to buy the product's features.

#### JTBD Statement Template

```
When [situation / context]
I want to [motivation / functional job]
So I can [expected outcome / emotional job]

Example:
When I need to report departmental budget execution to the CFO at month-end
I want to quickly generate a visualization report with YoY / MoM / budget variance
So I can complete report preparation within 30 minutes, without manually pulling data from 5 systems
```

#### Four-Dimensional Analysis

| Dimension | Analysis Question |
|------|---------|
| **Time Urgency** | How often does this job need to be done? What are the consequences of delay? |
| **Decision Level** | Who makes this decision? Individual / team / organization? |
| **Input Barriers** | What inputs are needed to complete this job? How hard are they to obtain? |
| **Output Requirements** | What format does the job output need? What precision is required? |

#### Job Card Template

| Field | Content |
|------|------|
| **JTBD ID** | JOB-001 |
| **Job Description** | [One-sentence description of the job the user needs to complete] |
| **Trigger Condition** | [Under what circumstances does the user need to complete this job] |
| **Success Criteria** | [What counts as done well] |
| **Current Solution** | [How the user does it now] |
| **Pain Points** | [Shortcomings of the current solution] |
| **Ideal Experience** | [The ideal state the user expects] |

#### B2B JTBD Examples

```
JTBD-001: Procurement Manager's Monthly Reconciliation
When I need to complete reconciliation of all last month's purchase orders before the 5th
I want to pull all supplier bills with one click and auto-match them to purchase orders
So I can complete reconciliation within 2 hours (originally took 2 days), with zero errors

JTBD-002: Sales Director's Pipeline Forecast
When I need to report the sales forecast to the CEO every Monday
I want to auto-generate a report with stage conversion rates and forecast accuracy from the CRM
So I can complete report preparation within 15 minutes, without manually aggregating data from 5 sales reps
```

### 2.9 B2B Sales Empowerment Methodology

#### Loss Analysis Framework

```
Loss Post-Mortem (complete within 48 hours after each deal loss):

1. Opportunity Basic Information
   - Customer name, industry, size
   - Opportunity stage, engagement duration
   - Competitor(s)

2. Key Decision Factors
   - Why did they choose the competitor over us?
   - Missing features? Price? Relationship? Brand?
   - If feature gap, what exactly was missing?

3. Our Performance
   - Did the demo impress?
   - Was there a problem with the sales strategy?
   - Was the PoC successful?

4. Product Implications
   - Is this feature gap universal or a one-off?
   - If one-off, should we build it or pass?
   - If a universal need, what is the priority?

5. Improvement Actions
   - Feature level: [specific action]
   - Sales level: [specific action]
   - Marketing level: [specific action]
```

#### Win Factor Analysis

```
B2B Key Win Factors (ranked by weight):
1. Product–Need Fit (30%)
2. Implementation & Delivery Capability (20%)
3. Sales Relationship & Trust (20%)
4. Price Competitiveness (15%)
5. Brand & Reputation (10%)
6. Technical / Security Capability (5%)
```

---

## 3. B2B Product Manager Competency Assessment

### B2B PM Competency Radar

```
        Business Acumen
             /\
            /  \
   Technical  /    \  User Research
  Understanding/      \
          /            \
         /______________\
    Data Analysis      Solution Design
          \            /
           \          /
            \        /
          Execution Power
```

### Specific Requirements by Competency Dimension

| Competency | Junior PM | Senior PM | Product Director |
|------|--------|--------|---------|
| **Business Acumen** | Understand business models | Design pricing and GTM | Define commercialization strategy |
| **User Research** | Conduct interviews | Design research plans | Build customer insight system |
| **Solution Design** | Write PRDs | System architecture design | Product portfolio architecture |
| **Data Analysis** | Read reports | Define metrics frameworks | Data-driven decision culture |
| **Technical Understanding** | Understand APIs | Participate in architecture discussions | Steer technical direction |
| **Execution Power** | Complete assigned tasks | Independently drive projects | Parallel management of multiple product lines |

---

## 4. B2B Product Anti-Patterns (Pitfall Avoidance Guide)

### Top 10 Common Mistakes

| Mistake | Manifestation | Correct Approach |
|------|------|---------|
| **Customizing for a Single Key Account** | Changing the product for one customer, turning into a project company | Stay product-oriented; customization via configuration / PaaS |
| **Feature Bloat** | Building everything competitors have | Focus on core value; compete on differentiation |
| **Ignoring Implementation & Delivery** | Great product but no one knows how to use it | Onboarding experience is equally important |
| **No Data Isolation** | Customer A sees Customer B's data | This is a fatal B2B mistake; must be designed from Day 1 |
| **Over-Engineered Permissions** | Dozens of roles, hundreds of permission points | MVP: least privilege set, expand incrementally |
| **Ignoring Audit Requirements** | No operation logs | B2B must record all critical operations |
| **Mobile as a Shrunken PC Version** | Approval forms with hundreds of fields on mobile | Mobile focuses on core high-frequency actions (approve / view / notify) |
| **Ignoring Exception Flows** | Only designing the happy path | Withdraw / reject / timeout / exception / concurrency must all be considered |
| **Over-Promising** | Saying yes to everything | Clearly define boundaries; explicitly decline what can't be done |
| **Building in an Ivory Tower** | Defining requirements without talking to customers | Every requirement should have customer input |