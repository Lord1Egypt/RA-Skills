# AI Product Pricing Plan Template

## Document Information

| Field | Content |
|------|------|
| Product Name | [Product Name] |
| Version | V1.0 |
| Date | YYYY-MM-DD |
| Author | [Name] |
| AI Product Type | AI-Native / AI-Enhanced / AI-Infrastructure |

---

## 1. Pricing Strategy Overview

### 1.1 Pricing Objectives

| Objective | Priority | Quantitative Target |
|------|--------|---------|
| Market Penetration | | |
| Revenue Maximization | | |
| Customer Retention (NRR) | | |
| AI Gross Margin Target | | >60% |
| Competitive Positioning | | |

### 1.2 AI Pricing Specifics

| Special Factor | Impact on Pricing | Mitigation Strategy |
|---------|------------|---------|
| Unpredictable Token Costs | Usage-based billing carries risk | Cost caps + model routing + caching |
| Continuously Improving Model Capabilities | Pricing must adapt to model upgrades | Versioned pricing + auto-upgrade clauses |
| Growing User Consumption | Costs may scale non-linearly | Tiered limits + overage tiered pricing |
| Intense Competition | Open-source models drive prices down | Differentiated value + data flywheel |
| Hard-to-Quantify Value | Customers struggle to assess ROI | Results-oriented pricing + free trial |

---

## 2. The 6 AI Pricing Models

### 2.1 Model Comparison

| Model | Description | AI Use Case | Pros | Cons | AI Product Example |
|------|------|-----------|------|------|-----------|
| **Subscription (SaaS)** | Fixed monthly/annual fee | AI-Enhanced products | Predictable revenue | Wide usage variance | GitHub Copilot $10/mo |
| **Usage-Based** | Per API call / Token / count | AI APIs / Platforms | Fair & transparent | Unpredictable costs | GPT-4 API |
| **Outcome-Based** | Per task completed by AI | Agent / Automation | Strong value alignment | Complex metering | Intercom Fin $0.99/resolution |
| **Hybrid** | Base fee + usage | AI-Native SaaS | Balances stability + elasticity | Complex pricing | Notion AI $10 + overage |
| **Value-Based** | Based on value created for customer | Vertical AI | ROI directly visible | Requires value quantification | Healthcare AI / per diagnosis |
| **Freemium** | Free features + paid premium AI | Individual → Enterprise conversion | Fast acquisition | Uncertain conversion rate | ChatGPT / Cursor |

### 2.2 Model Selection Decision Tree

```
Is AI functionality core to the product?
├── Yes → Is AI cost share high (>30%)?
│       ├── Yes → Is customer usage variance high?
│       │       ├── Yes → Hybrid Pricing (base + usage)
│       │       └── No → Usage-Based Pricing
│       └── No → Subscription Pricing (AI as value-add feature)
└── No → AI is auxiliary
          └── Subscription (with AI quota) + AI usage overage fees
```

---

## 3. Token Economics

### 3.1 Cost Structure Analysis

| Cost Item | Calculation Method | Monthly Cost | Share |
|--------|---------|---------|------|
| LLM API Calls (Input) | $X/1M tokens × monthly input volume | | |
| LLM API Calls (Output) | $Y/1M tokens × monthly output volume | | |
| Embedding API | $Z/1M tokens × monthly volume | | |
| Reranker API | | | |
| Vector Database | Storage + queries | | |
| GPU / Inference Servers (if self-deployed) | | | |
| Other AI Infrastructure | | | |
| Non-AI Costs (servers / bandwidth / labor) | | | |
| **Total Cost** | | | |

### 3.2 Per-User Token Consumption Model

| User Type | Daily Interactions | Avg Input per Interaction | Avg Output per Interaction | Daily Tokens | Monthly Tokens | Monthly Cost |
|---------|------------|----------|-----------|----------|----------|--------|
| Light User | | | | | | |
| Standard User | | | | | | |
| Heavy User | | | | | | |
| Power User | | | | | | |

### 3.3 Cost Optimization Levers

| Optimization Lever | Estimated Savings | Implementation Complexity | Side Effects |
|---------|---------|-----------|--------|
| Prompt Caching | 30-50% | Low | Only effective for repeated prefixes |
| Model Routing (simple → small model) | 40-60% | Medium | Complex cases may be misrouted |
| Semantic Caching (similar queries) | 20-40% | Medium-High | Not suitable for time-sensitive needs |
| Output Token Limits | 10-20% | Low | May truncate useful output |
| Fine-tuned Small Model Replacing Large Model | 50-80% | High | Requires training data + maintenance |
| Batch Processing (non-real-time scenarios) | 50% | Medium | Increased latency |

### 3.4 AI Gross Margin Calculation

```
AI Gross Margin = (Revenue - AI Inference Cost - AI Infrastructure Cost) / Revenue × 100%

Example Calculation:
- Monthly Fee: $30/user
- Monthly Token Consumption: 500K input + 100K output
- Model Cost (GPT-4o): $2.5/1M input + $10/1M output
- Monthly AI Cost: 500K/1M × $2.5 + 100K/1M × $10 = $1.25 + $1.00 = $2.25
- AI Gross Margin: ($30 - $2.25 - $3 infrastructure) / $30 = 82.5% ✅

Target: AI Gross Margin > 60%
```

---

## 4. Plan Design

### 4.1 Plan Structure

| Item | Free | Starter | Professional | Enterprise |
|------|------|---------|-------------|------------|
| Price | $0/mo | $X/mo | $Y/mo | Custom Quote |
| AI Interactions | 10/day | 100/mo | 500/mo | Unlimited |
| Model Tier | Basic Model | Standard Model | Advanced Model | Custom Model |
| Context Length | 4K | 16K | 128K | Custom |
| RAG Knowledge Bases | - | 1 | 5 | Unlimited |
| Agent Capabilities | - | Basic Agent | Advanced Agent | Custom Agent |
| HITL Control | Autonomous Only | Configurable | Fine-Grained Control | Full Control |
| API Access | - | - | ✓ | ✓ |
| Private Deployment | - | - | - | ✓ |
| SSO | - | - | ✓ | ✓ |
| Audit Logs | - | - | ✓ | ✓ |
| SLA | - | 99.5% | 99.9% | 99.95% |
| Support | Community | Email | Priority | Dedicated CSM |

### 4.2 Plan Upgrade Triggers

| Metric | Free→Starter Trigger | Starter→Pro Trigger | Pro→Enterprise Trigger |
|------|-----------------|----------------|-------------------|
| AI Usage | >10/day avg | >100/mo avg | >500/mo avg |
| Knowledge Base Count | - | >1 | >5 |
| Collaborator Count | - | >5 people | >20 people |
| Feature Requirements | Agent / RAG | Advanced Agent | Customization |

### 4.3 AI Quota Design

| Quota Model | Description | Pros & Cons |
|---------|------|--------|
| Hard Limit | Service stops when quota reached | Simple but poor UX |
| Soft Limit | Overage downgrades quality (smaller model) | Smooth experience |
| Overage Billing | Pay per use beyond quota | Flexible but requires user understanding |
| Feature Downgrade | Overage restricts advanced features | Controlled experience |

---

## 5. Competitive Pricing

### 5.1 AI Competitor Pricing Comparison

| Competitor | Free Tier | Entry Price | Core Price | Enterprise Price | Pricing Model | AI Cost Coverage |
|------|--------|--------|--------|--------|---------|----------|
| | | | | | | |

### 5.2 Pricing Positioning Strategy

| Strategy | Description | Applicable Scenario |
|------|------|---------|
| Penetration Pricing | Below competitors to attract users | Early market, strong network effects |
| Skimming Pricing | Above competitors emphasizing quality | Technology leadership, strong brand |
| Value-Based Pricing | Priced by value created | Vertical industries, clear ROI |
| Competitive Pricing | Match competitor prices | Homogeneous features |

---

## 6. AI Free Tier Strategy

### 6.1 AI Free Tier Design Principles

| Principle | Description |
|------|------|
| Showcase AI Core Value | Free tier must let users experience AI's "magic moment" |
| Control Free Costs | Free user AI cost < customer acquisition cost |
| Natural Conversion Design | Trigger payment at the moment of real need (not arbitrary limits) |
| Usage Limits Over Feature Limits | "You've used today's free quota" is better than "This feature requires payment" |
| Individual → Team Conversion | Free tier cultivates individual users → paid team conversion |

### 6.2 Free Tier Cost Control

| Method | Description |
|------|------|
| Use Cheaper Models | Free uses GPT-4o-mini, Pro uses GPT-4o |
| Lower Token Limits | Restrict context length and output length |
| Delayed / Downgraded Processing | Free requests get lower queue priority |
| Cache-First | Free requests prioritize cached results |
| Ads / Watermarks | Non-paying user outputs carry brand watermark |

---

## 7. Outcome-Based Pricing Deep Dive

### 7.1 Applicability Checklist

```
The more conditions below are met, the more suitable outcome-based pricing is:
□ AI completes a full task, not just assistance
□ Task results are clearly definable and verifiable
□ Task value is quantifiable (how much labor/time saved)
□ Customer trust in AI is sufficiently high
□ AI success rate and cost are predictable
□ Competitive landscape suits differentiated pricing
```

### 7.2 Outcome Definition Examples

| Product Type | Billing Unit | Outcome Definition | Verification Method |
|---------|---------|---------|---------|
| AI Customer Service | Resolved tickets | User marks as "Resolved" | User feedback + system judgment |
| AI Recruiting | Screened candidates | Entered interview stage | ATS system callback |
| AI Legal | Reviewed contracts | Review report completed | User confirms receipt |
| AI Code | Merged PRs | Code merged | Git webhook |
| AI Marketing | Qualified leads generated | MQL criteria met | CRM status change |

---

## 8. Sales Pricing Strategy

### 8.1 Common B2B Sales Tactics

| Tactic | Description | AI Product Fit |
|------|------|-------------|
| Annual Discount | 10-20% off for annual billing | ✅ Recommended (lock in customers + reduce churn) |
| Volume Discount | Lower unit price with more users | ✅ Suitable for team products |
| Committed-Use Discount | Discount for prepaid tokens / count | ✅ Suitable for API products |
| Free PoC | 3-month free pilot | ✅ Essential for B2B AI products |
| Bundling | Bundle with existing products | ✅ e.g. Office + AI |
| Seed-Stage Pricing | Special pricing for early customers in exchange for feedback | ✅ Early-stage AI products |

### 8.2 AI Product PoC Strategy

```
PoC Design Elements:
├── Duration: 30-90 days (depending on scenario complexity)
├── Scope: Select 1-2 scenarios that best demonstrate AI value
├── Success Criteria: Jointly define quantifiable success metrics with the customer
├── Data Access: Clarify which data can be used during PoC
├── Conversion Terms: Agreed-upon paid conversion plan upon PoC success (pre-negotiated)
└── Security & Compliance: Data handling and NDA during PoC
```

---

## 9. International Pricing

### 9.1 Regional Pricing Coefficients

| Region | Pricing Coefficient | Rationale |
|------|---------|------|
| North America | 1.0x (baseline) | Highest willingness to pay |
| Western Europe | 0.9x | High willingness to pay |
| Japan | 0.9x | High willingness to pay |
| Southeast Asia | 0.5x | Low willingness to pay but large market |
| India | 0.4x | Very low willingness to pay |
| China | 0.6x | Intense competition |

### 9.2 Regional Differences in AI Costs

| Factor | Impact |
|------|------|
| Model API Regional Pricing | OpenAI / Anthropic pricing differs in some regions |
| Localization Prompt Cost | Non-English prompts consume more tokens |
| Data Localization Requirements | Private deployment increases costs |
| Compliance Costs | Different compliance requirements across regions |

---

## 10. Pricing Experiments

### 10.1 A/B Test Design

| Test Dimension | Variant A | Variant B | Core Metric |
|---------|-------|-------|---------|
| Price Point | $X/mo | $Y/mo | Paid conversion rate × ARPU |
| Billing Model | Subscription | Usage-Based | Total ARPU |
| Plan Structure | 3 tiers | 4 tiers | Paid conversion rate |
| Free Quota | X/day | Y/day | Conversion rate + retention |
| Pricing Anchor | Show most expensive plan | Don't show | Mid-tier selection rate |

### 10.2 Pricing Sensitivity Test

```
Van Westendorp Price Sensitivity Model:
Q1: At what price would you consider it too cheap and question quality? → PMC (Point of Marginal Cheapness)
Q2: At what price would you consider it a bargain?                       → PME (Point of Marginal Expensiveness)
Q3: At what price would you start to feel it's expensive?                → IDP (Indifference Price Point)
Q4: At what price would you consider it too expensive to accept?         → OPP (Optimal Price Point)

Optimal price range: IDP ~ OPP
```

---

## 11. Revenue Model

### 11.1 Key Metrics

| Metric | Calculation | Target |
|------|---------|--------|
| ARPU | Total Revenue / Paid Users | |
| ARPA | Total Revenue / Paid Accounts | |
| LTV | ARPU × Average Lifetime (months) | |
| CAC | Total Sales & Marketing Spend / New Customers | |
| LTV/CAC | | >3x |
| Paid Conversion Rate | Paid Users / Total Users | |
| Monthly Churn Rate | Churned Users / Beginning-of-Month Users | <3% |
| NRR | (Beginning ARR + Expansion - Churn) / Beginning ARR | >100% |
| AI Gross Margin | (Revenue - AI Costs) / Revenue | >60% |

### 11.2 3-Year Revenue Forecast

| Year | Year 1 | Year 2 | Year 3 |
|------|--------|--------|--------|
| Total Users | | | |
| Paid Users | | | |
| Paid Conversion Rate | | | |
| ARPU | | | |
| Annual Revenue (ARR) | | | |
| Total AI Costs | | | |
| AI Gross Margin | | | |
| Total Gross Margin | | | |

---

## v1.1.0 Added: Model Cost Considerations

### Mainstream Model Cost Comparison (2026 Reference)
| Model | Input Price | Output Price | Use Case |
|------|---------|---------|---------|
| GPT-4o | $2.5/1M tokens | $10/1M tokens | Complex reasoning |
| GPT-4o-mini | $0.15/1M tokens | $0.6/1M tokens | Simple tasks |
| Claude 3.5 Sonnet | $3/1M tokens | $15/1M tokens | Long-form text |
| Claude 3.5 Haiku | $0.25/1M tokens | $1.25/1M tokens | Fast responses |
| Qwen-Max (Domestic) | ¥0.02/1K tokens | ¥0.06/1K tokens | Chinese-language scenarios |
| DeepSeek-V3 (Domestic) | ¥0.001/1K tokens | ¥0.002/1K tokens | High cost-effectiveness |

### Model Cost Optimization Strategies
| Strategy | Savings Rate | Applicable Scenario |
|------|---------|---------|
| Model Routing (small model → large model) | 40-60% | Tiered processing |
| Cache Common Queries | 30-50% | Repeated questions |
| Prompt Compression | 20-30% | Long contexts |
| Batch Processing | 10-20% | Non-real-time scenarios |
| Fine-tuned Small Model Replacing Large Model | 50-80% | Vertical domains |