# Enterprise Procurement System — Complete Business Analysis Case

> This case demonstrates a full end-to-end business analysis process for an enterprise-grade procurement system, from 0 to 1.
> Covering: Strategic Analysis → Market Insights → Financial Modeling → Requirements Engineering → Business Case → Implementation Roadmap.

---

## Case Background

### Company Overview
- Company: A large manufacturing conglomerate (annual revenue ¥5 billion, 8,000 employees)
- Challenge: Fragmented procurement processes, opaque data, chaotic supplier management
- Sponsor: CPO (Chief Procurement Officer), with strong attention from the CFO
- BA Objective: Complete procurement system business analysis + business case within 3 months to support the board's investment decision

### Current Pain Point Scoring

| Pain Point | Severity | Frequency | Annualized Loss (Est.) |
|------------|----------|-----------|------------------------|
| Procurement spread across 6 systems + Excel | 5 | Daily | 4,500 person-hours/year |
| Inconsistent supplier data — same supplier under 5 different names | 4 | Ongoing | Hard to quantify but severely impacts decision-making |
| No digital price comparison / bidding | 4 | Monthly | Estimated 5–8% higher procurement costs |
| Lengthy approval process (paper + email) | 3 | Per order | 30% longer procurement cycle |
| Difficult compliance auditing | 3 | Quarterly audits | 2 compliance incidents per year |

---

## Phase 1: Strategy & Industry Analysis

### PESTLE Key Findings

| Dimension | Key Finding | Impact on Project |
|-----------|-------------|-------------------|
| Political | SASAC pushing digital transformation for central/SOE procurement | Executive support, policy tailwind |
| Economic | Manufacturing margins under pressure; urgent need for cost reduction and efficiency improvement | Procurement savings = direct profit contribution |
| Social | Younger-generation buyers more accustomed to digital tools | Good system adoption |
| Technology | Cloud-based procurement SaaS is mature; AI supplier matching available | Low technical risk |
| Legal | Electronic Bidding Law + Electronic Signature Law now well-established | Compliance supports digitalization |

### Industry Lifecycle Assessment
**Enterprise Procurement SaaS**: Growth stage (market growth >25%/year, rapidly increasing competitors)

### KSF (Key Success Factors)

| KSF | Importance | Rationale |
|-----|------------|-----------|
| Supplier network coverage | Extremely High | Core value of procurement comes from supplier resources |
| Flexible, configurable processes | High | Procurement workflows vary greatly across industries |
| System integration capability (ERP/WMS) | High | Procurement is not a silo — must integrate with multiple systems |
| Compliance & audit functionality | High | Procurement is a high-frequency compliance risk area |

---

## Phase 2: Market & Customer Insights

### Market Sizing (TAM-SAM-SOM)

```
TAM (Manufacturing procurement digitalization) = 400,000 above-scale manufacturers × ¥200K/year = ¥80 billion
SAM (Mid-to-large enterprises with sufficient budget) = ¥80 billion × 30% = ¥24 billion
SOM (Attainable within 3 years) = ¥24 billion × 5% = ¥1.2 billion
```

### Internal User Personas

| Role | Headcount | Core Needs | Core Pain Points | Attitude Toward Change |
|------|-----------|------------|------------------|------------------------|
| Buyers | 120 | Quickly find suppliers, compare prices, place orders | Switching between 6 systems, manual price comparison | ⭐⭐⭐⭐ Supportive (frees them from repetitive work) |
| Procurement Managers | 18 | Approval, control, reporting | Opaque approval process, exhausting Excel consolidation | ⭐⭐⭐⭐⭐ Very supportive |
| Supplier Management | 8 | Supplier evaluation / tiering / performance | Inconsistent data, no unified view | ⭐⭐⭐ Supportive with reservations |
| Finance Department | 15 | Invoice matching, payment approval | Manual three-way matching, high error rate | ⭐⭐⭐ Supportive |
| Legal / Compliance | 5 | Compliance review, audit trail | Audits require digging through piles of paper documents | ⭐⭐⭐⭐⭐ Very supportive |

---

## Phase 3: Competitive Analysis

### Competitor Assessment (Simplified)

| Competitor | Positioning | Target Customers | Strengths | Weaknesses |
|------------|-------------|------------------|-----------|------------|
| SAP Ariba | Global leader | Large multinationals | Largest supplier network | Expensive + slow implementation + weak localization |
| Coupa | Cloud-native | Mid-to-large enterprises | Great UX, fast implementation | Weak supplier network in China |
| Zhenyun Technology | China procurement SaaS | Mid-to-large Chinese enterprises | Strong Chinese-language support, localized | Insufficient functional depth |
| Yonyou Procurement Cloud | ERP-integrated | Yonyou ERP customers | Strong integration | Mediocre experience for non-Yonyou customers |
| Self-built | Fully custom | Companies with IT capability | Full control | High cost, long timeline |

---

## Phase 4: Financial Analysis

### TCO Comparison (3-Year)

| Cost Item | Self-built | SAP Ariba | Coupa | Zhenyun | Yonyou |
|-----------|------------|-----------|-------|---------|--------|
| Initial investment | ¥12M | ¥3M | ¥2M | ¥1.8M | ¥2.2M |
| Annual operating cost | ¥2M | ¥3.5M | ¥2.5M | ¥1.8M | ¥2M |
| 3-Year TCO | ¥18M | ¥13.5M | ¥9.5M | ¥7.2M | ¥8.2M |

### Benefit Estimates (Zhenyun Scenario)

| Benefit Source | Year 1 | Year 2 | Year 3 | Realization Approach |
|----------------|--------|--------|--------|----------------------|
| Procurement cost savings (via price comparison / centralized purchasing) | ¥1.5M | ¥3.5M | ¥5M | Price transparency + centralized procurement |
| Labor efficiency savings | ¥1.2M | ¥1.8M | ¥2M | Process automation |
| Compliance risk reduction | ¥0.5M | ¥0.8M | ¥1M | Electronic audit trail |
| **Total Annual Benefits** | **¥3.2M** | **¥6.1M** | **¥8M** | |

### Return on Investment

```
Total Investment (3-Year TCO): ¥7.2M
3-Year Cumulative Benefits: ¥17.3M
NPV (discount rate 10%): ¥6.28M
IRR: 68%
Payback Period: 18 months
ROI (3-Year): 140%
```

---

## Phase 5: Stakeholder Analysis

### Power-Interest Matrix

```
High Power:
- CEO: High interest → Manage closely. Focus on ROI, strategic alignment, risk
- CFO: High interest → Manage closely. Focus on TCO, cash flow, audit
- CPO (Sponsor): High interest → Manage closely. Project success directly impacts their KPIs

Medium Power:
- IT Director: High interest → Manage closely. Focus on technical feasibility, integration complexity
- Procurement Manager Lead: High interest → Keep informed + engaged. Focus on daily work efficiency
- Finance Director: Medium interest → Keep satisfied. Focus on payment processes, reconciliation automation

Low Power:
- Frontline Buyers: High interest → Keep informed. Focus on usability
- Legal: Medium interest → Keep informed. Focus on electronic contract compliance
```

### Key Person Deep-Dive: CFO

| Dimension | Analysis |
|-----------|----------|
| KPIs | Cost control, ROIC, cash flow, zero audit findings |
| Decision Style | Data-driven + risk-averse |
| Possible Objections | TCO exceeds budget? Can benefits actually be realized? |
| Influence Strategy | Emphasize financial model + NPV under conservative scenario + risk mitigation |
| One-liner to win them over | "3-year procurement cost savings of ¥10.3M, while reducing compliance risk by 90%" |

---

## Phase 6: Requirements Analysis

### Requirements Hierarchy

**Business Requirement:**
"Establish a unified digital procurement platform to achieve full-process transparency and standardization, reducing total procurement cost by 5–8% within 3 years."

**Functional Requirements — Top 10:**

| ID | Function | Priority | Linked Pain Point |
|----|----------|----------|-------------------|
| FR-01 | Supplier management (onboarding / evaluation / tiering / performance) | Must | Inconsistent data |
| FR-02 | Purchase requisition & approval workflow | Must | Lengthy approvals |
| FR-03 | RFQ price comparison / bidding management | Must | Opaque pricing |
| FR-04 | Purchase order management | Must | Fragmented systems |
| FR-05 | Contract management | Must | Paper contracts |
| FR-06 | Goods receipt & acceptance | Should | — |
| FR-07 | Invoice verification & three-way matching | Should | Manual matching |
| FR-08 | Data analytics & BI reporting | Should | Excel consolidation |
| FR-09 | Mobile approval | Could | Business travel scenarios |
| FR-10 | AI supplier intelligent recommendation | Could | Difficulty finding suppliers |

### MoSCoW Prioritization

Applying the MoSCoW method for rigorous priority ranking of functional requirements, ensuring the Minimum Viable Product focuses on core value:

| Level | Functions | Share | Rationale |
|-------|-----------|-------|-----------|
| **Must Have** | FR-01~FR-05 (supplier management, approval workflow, RFQ/bidding, order management, contract management) | 50% | Without these, the procurement system cannot function; directly addresses core pain points like "fragmented systems" and "opaque pricing" |
| **Should Have** | FR-06~FR-08 (goods receipt/acceptance, invoice verification, data analytics) | 30% | Important but not fatal: acceptance and invoicing can use manual workarounds, BI can initially be replaced by Excel exports |
| **Could Have** | FR-09~FR-10 (mobile approval, AI recommendations) | 20% | Nice-to-have: mobile addresses travel scenarios, AI recommendations require data accumulation before delivering value |
| **Won't Have** | Supplier collaboration portal, deep SRM features | Excluded | This phase focuses on procurement execution; supplier collaboration is slated for Phase 2 |

> **MoSCoW Application Insights**: Must Have is capped at 50% (≤60% threshold), ensuring team focus. "Won't Have" does not mean "never" — it means "not this time." The supplier collaboration portal is already on the Phase 2 roadmap. Prioritization was jointly confirmed by the CPO and procurement manager lead, avoiding unilateral judgment by the BA.

---

## Phase 7: Business Case

### Executive Summary (Board-Level Version)

> **Problem**: The group's procurement processes are scattered across 6 systems plus extensive Excel usage, with annualized procurement cost losses of 5–8%, over 4,500 hours wasted annually on manual processes, and 2 compliance audit issues in the past 2 years.
>
> **Solution**: Deploy Zhenyun Technology's digital procurement platform, complete implementation within 12 months, covering procurement operations group-wide.
>
> **Value**: 3-year investment of ¥7.2M, projected cumulative benefits of ¥17.3M, NPV ¥6.28M, IRR 68%, 18-month payback. Compliance risk reduced by 90%.
>
> **Request**: Approve ¥7.2M budget, authorize the CPO to form the project team, and launch implementation in Q2.

### Recommended Options (3 Options + Do Nothing)

| Evaluation Dimension (Weight) | Zhenyun (Recommended) | Yonyou | Self-built | Do Nothing |
|-------------------------------|----------------------|--------|------------|------------|
| TCO 3-Year (25%) | 7.2M | 8.2M | 18M | Status quo cost |
| Functional Fit (25%) | 4 | 4 | 5 | 0 |
| Implementation Speed (20%) | 4 | 3 | 1 | 5 |
| Supplier Network (15%) | 4 | 3 | 0 | 0 |
| Risk (15%) | 3 | 3 | 1 | 5 |
| **Weighted Total Score** | **3.80** | **3.35** | **1.90** | **2.75** |

---

## Phase 8: Implementation Roadmap

| Phase | Timeline | Content | Key Deliverables |
|-------|----------|---------|------------------|
| Phase 0: Preparation | Month 1–2 | Vendor contracting + project team + environment setup | Contract + team + project plan |
| Phase 1: Blueprint Design | Month 3–4 | Business process mapping + requirements confirmation | Blueprint document + requirements matrix |
| Phase 2: System Implementation | Month 5–8 | Configuration, development, integration + testing | UAT sign-off |
| Phase 3: Pilot | Month 9–10 | Pilot in 2 business units | Pilot success + feedback & fixes |
| Phase 4: Rollout | Month 11–14 | Group-wide rollout + training | All-staff go-live |
| Phase 5: Stabilization | Month 15–18 | Legacy system decommissioning + optimization | KPIs met |

---

## BA Value Summary

| Phase | Key BA Contribution | Without a BA |
|-------|---------------------|--------------|
| Strategic Analysis | Confirmed procurement digitalization is a strategic-level opportunity | Might have chosen the wrong direction or missed this opportunity entirely |
| Market Analysis | Quantified market size + internal user needs | No benchmark for evaluating external solutions |
| Competitive Analysis | Comprehensive comparison of 5 options with reasoned recommendation | Might have chosen the most famous or the cheapest option |
| Financial Analysis | Precise TCO + ROI model | Gut-feel judgment; CFO would not have approved |
| Stakeholder Analysis | Identified CFO as key + targeted influence strategy | Project could have been vetoed by the CFO |
| Requirements Analysis | Top 10 functions + MoSCoW prioritization | Would have bought whatever the vendor said was needed |
| Business Case | Board-level investment recommendation + NPV/IRR | Could not answer "why now" |