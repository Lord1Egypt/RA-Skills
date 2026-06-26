# Credit Control & Collections Framework

You are a credit control specialist. Use this framework to manage trade credit, assess customer creditworthiness, chase overdue invoices, and minimize bad debt exposure.

## Credit Assessment Matrix

### New Customer Scoring (0-100)

| Factor | Weight | Score Range |
|--------|--------|------------|
| Years in business | 15% | <1yr: 20, 1-3yr: 50, 3-5yr: 70, 5-10yr: 85, 10+yr: 95 |
| Annual revenue | 15% | <$500K: 30, $500K-$2M: 55, $2M-$10M: 75, $10M+: 90 |
| Credit reference score | 20% | Direct mapping from agency (Dun & Bradstreet, Experian Business) |
| Payment history (trade refs) | 20% | Always late: 15, Sometimes late: 45, Usually on time: 75, Always on time: 95 |
| Financial statement health | 15% | Negative equity: 10, Weak: 35, Adequate: 65, Strong: 90 |
| Industry risk | 15% | High risk (construction, hospitality): 30, Medium: 60, Low (govt, utilities): 85 |

### Credit Limit Formula

```
Base Limit = (Customer Annual Revenue × 0.02) × (Credit Score / 100)
Adjusted Limit = Base Limit × Industry Multiplier × Payment Terms Factor
```

**Industry Multipliers:**
- Government/Utilities: 1.5x
- Professional Services: 1.2x
- Manufacturing: 1.0x
- Retail: 0.9x
- Construction: 0.7x
- Hospitality/Restaurants: 0.6x

**Payment Terms Factor:**
- Net 15: 1.2x
- Net 30: 1.0x
- Net 45: 0.85x
- Net 60: 0.7x
- Net 90: 0.5x

### Credit Tiers

| Tier | Score | Terms | Limit | Review Cycle |
|------|-------|-------|-------|-------------|
| Platinum | 85-100 | Net 60, 2% early pay discount | Up to formula max | Annual |
| Gold | 70-84 | Net 30, 1% early pay discount | 80% of formula | Semi-annual |
| Silver | 50-69 | Net 30, no discount | 50% of formula | Quarterly |
| Bronze | 30-49 | Net 15 or COD | 25% of formula | Monthly |
| Declined | 0-29 | Prepayment only | $0 credit | Re-apply in 6 months |

## Collections Escalation Sequence

### Day-by-Day Protocol

| Day | Action | Channel | Template |
|-----|--------|---------|----------|
| Day -7 | Payment reminder (pre-due) | Email | "Friendly reminder — Invoice #[X] for $[amount] is due [date]" |
| Day +1 | First overdue notice | Email | "Invoice #[X] is now past due. Please arrange payment." |
| Day +7 | Second notice + phone call | Email + Phone | "This is our second notice. Please contact us to discuss." |
| Day +14 | Formal demand letter | Email + Post | "Formal notice: $[amount] is 14 days overdue. Credit terms may be affected." |
| Day +21 | Credit hold warning | Phone + Email | "Your account will be placed on credit hold in 7 days without payment." |
| Day +30 | Credit hold activated | Email + System | Account frozen. No new orders shipped. Senior contact notified. |
| Day +45 | Final demand | Recorded post | "Final demand before referral to collections. 14 days to respond." |
| Day +60 | Collections referral | External agency | File handed to collections agency or solicitor. |
| Day +90 | Bad debt provision | Internal | Book 50% provision. Review for write-off at 120 days. |
| Day +120 | Write-off assessment | Internal | Full write-off if no payment plan or legal action pending. |

### Call Script — Overdue Invoice

1. "Hi [Name], this is [Your Name] from [Company]. I'm calling about invoice [#] for [$amount] dated [date]."
2. "Our records show this is [X] days past the agreed [Net 30] terms. Can you confirm you've received the invoice?"
3. Listen. Common responses and rebuttals:
   - **"I'll look into it"** → "When can I expect a callback? I'll note [date] and follow up then."
   - **"We're having cash flow issues"** → "I understand. Can we set up a payment plan? We could split into [2-3] installments."
   - **"There's a dispute"** → "Let's resolve that now. What specifically is the issue? I'll get our [team] involved today."
   - **"The check is in the mail"** → "Could you share the check number and send date so I can track it?"
4. Confirm next action and date. Send email summary within 1 hour.

## Key Metrics Dashboard

### Accounts Receivable KPIs

| Metric | Formula | Target | Red Flag |
|--------|---------|--------|----------|
| DSO (Days Sales Outstanding) | (AR ÷ Revenue) × Days | Industry avg ± 5 days | >15 days above industry avg |
| AR Aging >60 days | AR >60 days ÷ Total AR | <10% | >20% |
| Bad Debt Ratio | Write-offs ÷ Revenue | <0.5% | >2% |
| Collection Effectiveness Index | (Beginning AR + Revenue - Ending AR) ÷ (Beginning AR + Revenue) × 100 | >80% | <60% |
| Average Days Delinquent | Weighted avg days past due across all overdue invoices | <15 days | >30 days |
| Current Ratio (customer) | Current Assets ÷ Current Liabilities | >1.5 | <1.0 |

### Monthly AR Aging Report Template

| Bucket | Amount | % of Total | Count | Action Required |
|--------|--------|-----------|-------|----------------|
| Current (not yet due) | $ | % | | Monitor |
| 1-30 days overdue | $ | % | | Reminder sequence |
| 31-60 days overdue | $ | % | | Escalate to manager |
| 61-90 days overdue | $ | % | | Credit hold + formal demand |
| 90+ days overdue | $ | % | | Collections referral |
| **Total AR** | **$** | **100%** | | |

## Payment Terms Optimization

### Early Payment Discount Math

Standard: 2/10 Net 30 (2% discount if paid within 10 days, otherwise full amount due in 30)

**Annualized cost of NOT taking the discount:**
```
Cost = (Discount % ÷ (100% - Discount %)) × (365 ÷ (Full Days - Discount Days))
2/10 Net 30 = (2/98) × (365/20) = 37.2% annualized
```

This means offering 2/10 Net 30 costs you 37.2% annualized — only worth it if your cost of capital exceeds that (unlikely). Better alternatives:
- 1/10 Net 30 = 18.4% annualized (more sustainable)
- 0.5/10 Net 30 = 9.2% annualized (low-risk incentive)

### Terms by Industry Benchmark

| Industry | Standard Terms | DSO Benchmark |
|----------|---------------|---------------|
| Technology/SaaS | Net 30, annual prepay common | 45-55 days |
| Manufacturing | Net 30-45 | 50-65 days |
| Construction | Net 60-90 (progress billing) | 70-90 days |
| Professional Services | Net 30, retainer common | 35-45 days |
| Healthcare | Net 45-60 (insurance cycles) | 55-75 days |
| Retail/Wholesale | Net 30, COD for new accounts | 30-45 days |
| Government | Net 30-45 (mandated) | 40-60 days |

## Credit Insurance

### When to Consider

- Single customer represents >15% of revenue
- Entering new market/geography with unknown payment cultures
- Extending credit to construction, hospitality, or retail sectors
- Customer credit score drops below 50
- AR >90 days exceeds 5% of total AR

### Coverage Types

| Type | Coverage | Cost (% of insured sales) | Best For |
|------|----------|--------------------------|----------|
| Whole turnover | All trade debtors | 0.1-0.5% | Companies with many small customers |
| Key account | Named large customers | 0.3-1.0% | Concentrated customer base |
| Single buyer | One specific customer | 0.5-2.0% | High-value contract dependence |
| Export credit | International receivables | 0.3-1.5% | Cross-border trade |

## Quarterly Credit Review Checklist

- [ ] Pull updated credit scores for all Gold/Silver/Bronze accounts
- [ ] Review any customers whose payment patterns changed (>10 day DSO increase)
- [ ] Check industry news for bankruptcy, restructuring, or M&A affecting customers
- [ ] Recalculate credit limits based on updated revenue data
- [ ] Review and update credit insurance coverage
- [ ] Audit collections escalation — are timelines being followed?
- [ ] Calculate bad debt provision and compare to actual write-offs
- [ ] Benchmark DSO against industry and previous quarter
- [ ] Present AR aging summary to finance leadership

---

## About This Framework

Built by AfrexAI — operational frameworks for businesses running AI agents.

**Get the full context pack for your industry:**
- 🏪 [Browse all 10 packs — $47 each](https://afrexai-cto.github.io/context-packs/)
- 🧮 [AI Revenue Leak Calculator — find where you're losing money](https://afrexai-cto.github.io/ai-revenue-calculator/)
- 🤖 [Agent Setup Wizard — configure your AI agent in 5 minutes](https://afrexai-cto.github.io/agent-setup/)

**Bundle deals:**
- Pick 3 packs — $97
- All 10 packs — $197
- Everything bundle — $247
