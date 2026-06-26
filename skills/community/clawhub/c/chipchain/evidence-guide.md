# Evidence Types & Confidence Caps

> Manufacturing a material and supplying it to a specific customer require
> completely different evidence. This guide classifies evidence types and
> sets hard caps on what confidence level each type can support.

## The Six Evidence Types

| # | Type | What it proves | Example |
|---|---|---|---|
| 1 | **Capability** | Company makes material X | Patent, product catalog, company website, facility announcement |
| 2 | **Customer hint** | Company has customers in segment Y | Revenue geography ("80% from semiconductor"), vague filing language ("leading domestic memory manufacturers") |
| 3 | **Qualification signal** | Company passed a customer's approval process | 通过客户验证, 进入供应链 (CN), 고객사 인증 통과 (KR), supplier award announcements |
| 4 | **Financial disclosure** | Company has named commercial relationship | DART 주요 거래처, EDINET 主要販売先 (>10% revenue), cninfo 前五名客户销售额, IPO prospectus with customer revenue tables |
| 5 | **Trade/customs data** | Material physically moved between countries | Comtrade bilateral flows, bill of lading databases (Panjiva), HS-code-level import/export records |
| 6 | **Circumstantial** | Indirect signal suggesting relationship | Environmental permits near fab clusters, job postings, SEMICON exhibitor categories, conference co-authorship, chemical registrations (K-REACH, ECHA) |

Types 1-4 come from the company or its regulator. Types 5-6 come from outside
the company's own disclosures. Higher-numbered types are generally stronger for
proving a specific supply relationship, but Type 1 (capability) is often the
easiest to find, which is why it gets mistaken for proof.

## Confidence Caps

Not all evidence is created equal. These caps override the general confidence
system: no amount of repetition can push a finding above its cap.

| Evidence available | Maximum confidence allowed |
|---|---|
| Capability only (they make it) | **SPECULATIVE** |
| Capability + circumstantial (near the fab, right SEMICON booth) | **MODERATE INFERENCE** |
| Capability + customer hint (revenue geography, vague filing) | **MODERATE INFERENCE** |
| Capability + qualification signal (passed verification) | **STRONG INFERENCE** |
| Capability + trade data showing bilateral flow | **STRONG INFERENCE** |
| Capability + financial disclosure naming the customer | **CONFIRMED** |
| Financial disclosure accessed this session with named customer | **CONFIRMED** |

Key rules:
- **Capability evidence alone can never exceed SPECULATIVE**, regardless of how
  many sources confirm the capability. Ten articles saying "Company A makes
  photoresist" still only prove capability.
- **Multiple weak types don't jump a tier.** Three pieces of circumstantial
  evidence (job posting + SEMICON booth + geographic proximity) stay at
  MODERATE INFERENCE. They don't combine into STRONG INFERENCE.
- **Independent types do stack.** Qualification signal + trade data flow =
  STRONG INFERENCE, because these are genuinely independent evidence channels.
- **Only a named commercial relationship (accessed this session) reaches
  CONFIRMED.** This means a filing, press article naming the customer, or
  official announcement you actually read.
- **Freshness matters.** A financial disclosure from 5 years ago may no longer
  reflect a current relationship. Note the date and consider whether events
  since then (export controls, localization drives) could have invalidated it.
- **When evidence types contradict, surface the contradiction.** Don't pick
  the higher-capping type and ignore the other. A trade data flow that
  contradicts a financial disclosure is a finding, not noise.
- **Trade data (Type 5) is country-to-country, not company-to-company.** A
  Comtrade flow showing HF moving from Japan to Korea does not prove which
  Japanese company shipped to which Korean fab. It narrows the field.

## Worked Examples

### Example 1: "Does Company X supply CMP slurry to TSMC?"

| Evidence found | Type | Cap |
|---|---|---|
| Company X product catalog lists CMP slurry products | Capability | SPECULATIVE |
| Company X exhibits in "CMP Materials" at SEMICON Taiwan | Circumstantial | MODERATE INFERENCE |
| Company X 招股说明书: "通过台积电验证" (passed TSMC verification) | Qualification | STRONG INFERENCE |
| Company X IPO prospectus 前五名客户: Customer A in Taiwan = 34% of revenue | Financial (coded) | STRONG INFERENCE |
| DigiTimes article: "Company X begins volume supply to TSMC for N3" | Financial/named | CONFIRMED |

Without the DigiTimes article, this relationship caps at STRONG INFERENCE.
The IPO prospectus strongly suggests TSMC but the customer is coded. Only the
named article takes it to CONFIRMED.

### Example 2: "Does Company Y supply photoresist to Samsung?"

| Evidence found | Type | Cap |
|---|---|---|
| Company Y patent on ArF immersion resist formulation | Capability | SPECULATIVE |
| Company Y 80% revenue from "semiconductor manufacturers" | Customer hint | MODERATE INFERENCE |
| Company Y and Samsung engineers co-author IEDM paper | Circumstantial | MODERATE INFERENCE |

Three pieces of evidence, but none cross the qualification or financial
threshold. This stays at MODERATE INFERENCE. The right next step is to search
DART for Company Y's 사업보고서 주요 거래처 section, or look for a supplier
award announcement.

## Relationship to Other Skill Components

- **Confidence levels** (SKILL.md): This guide adds evidence-type caps to the
  existing system. The confidence levels still apply; this constrains which
  levels are reachable given the evidence you have.
- **Counterfactual check** (queries/counterfactual-check.md): Run the
  counterfactual AFTER applying these caps. A finding that passes the
  counterfactual but only has capability evidence still caps at SPECULATIVE.
- **Source Registry** (Phase 1): When building the registry, mentally tag each
  source by evidence type. This helps during Phase 2 when assigning confidence.
- **Triangulation playbook** (SKILL.md): The ten triangulation methods map onto
  evidence types. Revenue geography = Type 2, patent co-filing = Type 6,
  supplier awards = Type 3, customs data = Type 5.
