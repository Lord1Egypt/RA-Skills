# Prompt: Financial Projections + Revenue Model

Generate a 3-year financial model with monthly Year 1 projections, annual Year 2-3 projections, break-even analysis, and key assumptions.

---

## Your Input

```
Business Name: [e.g., FitTrack]
Revenue Model: [subscription | one-time | usage-based | services | hybrid — describe]
Pricing Tiers: [e.g., "Free (0), Pro ($29/mo), Agency ($79/mo)"]
Estimated Customer Acquisition Cost (CAC): [e.g., "$45 blended (paid social + organic)"]
Monthly Churn Rate: [e.g., "3% — estimate if unsure"]
Estimated Monthly Overhead: [e.g., "$800/month: hosting $200, tools $150, ads $450"]
Funding Amount: [e.g., "$50,000" or "Bootstrapped ($0)"]
Current MRR/Revenue: [e.g., "$0 (pre-launch)" or "$1,200 MRR"]
Target Market Size: [from your market analysis, e.g., "150,000 US independent trainers"]
Growth Strategy: [e.g., "paid social + referral program + SEO content"]
```

---

## Prompt

You are a financial analyst and startup CFO who builds models for early-stage companies. Generate a financial projections section for this business plan.

**Business:** [Business Name]
**Revenue Model:** [Revenue Model]
**Pricing:** [Pricing Tiers]
**CAC:** [CAC]
**Monthly Churn:** [Churn Rate]
**Monthly Overhead:** [Monthly Overhead]
**Funding:** [Funding Amount]
**Starting Revenue:** [Current MRR/Revenue]
**Market Size:** [Target Market Size]
**Growth Strategy:** [Growth Strategy]

Generate the following:

---

### 1. Revenue Model Summary (100 words)
Explain the revenue model in plain English: how the business makes money, the pricing structure, and the unit economics story (LTV vs. CAC). Include:
- **LTV calculation:** Average Revenue Per User × (1 / Monthly Churn Rate) = LTV
- **LTV:CAC ratio** and what it means for the business

### 2. Key Financial Assumptions
List all assumptions as a numbered table:

| # | Assumption | Value | Rationale |
|---|-----------|-------|-----------|

Include assumptions for: starting customers, monthly new customer acquisition (Month 1-6), monthly growth rate (Month 7-12), average revenue per user, churn rate, overhead breakdown, COGS (if applicable), and funding deployment schedule (if funded).

### 3. Monthly Revenue Projections — Year 1

Create a table with these columns:
| Month | New Customers | Churned | Total Customers | MRR | Cumulative Revenue |

Show Month 1 through Month 12. Use the assumptions above. Show realistic ramp (slow start, accelerating growth).

After the table, add a one-sentence summary of where the business is at end of Year 1.

### 4. Annual Projections — Years 1-3

| Year | Customers (EOY) | ARR | Gross Margin | Operating Expenses | Net Income / (Loss) |
|------|----------------|-----|-------------|-------------------|---------------------|

Include realistic growth rates for Years 2-3 (typically 150-300% YoY for early-stage SaaS).

### 5. Break-Even Analysis
Calculate and state:
- **Monthly break-even:** the MRR needed to cover monthly overhead
- **Customer break-even:** how many paying customers at average ARPU covers overhead
- **Timeline to break-even:** based on the Year 1 projections, which month does the business hit break-even?

### 6. Use of Funds (if funded)
If funding > $0, create a breakdown table:
| Category | Amount | % of Raise | Purpose |

If bootstrapped, skip this section.

### 7. Financial Risks + Mitigations (3-4 bullets)
Key financial risks (churn, CAC inflation, slow growth) and specific mitigations.

---

**Tone:** Precise, realistic, investor-grade. Avoid hockey-stick projections without justification. Show conservative, base, and optimistic cases for Year 3 ARR.  
**Format:** Use the headers and tables above. All numbers must be internally consistent.
