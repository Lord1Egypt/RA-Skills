# Evidence Hierarchy and Claim Boundaries for FAERS Output

> 中文摘要：FAERS 结论的四层证据分级（信号级 / 对比表征级 / 稳健性级 / 禁止推断区），以及每层"能说什么、不能说什么"。ct-safety 的每份输出都必须给结论打上证据层级标签。
>
> **Adapted from**: `active-comparator-single-soc-faers-safety-comparison` (references/validation-evidence-hierarchy.md, workload-configurations.md) — AIPOCH, MIT License
> **Source**: https://github.com/aipoch/medical-research-skills
> **Migrated**: 2026-08-04 (into ct-safety)

---

## Core principle

FAERS-based analyses produce **different kinds of evidence**. They must never be mixed in one undifferentiated conclusion. Every material result in a `ct-safety` report carries an explicit tier label.

---

## Tier 1 — Signal-detection-level evidence

**Supports**

- A drug (or drug group) is disproportionately reported together with an event or event family.
- The signal is stronger / weaker under a declared metric (PRR, ROR, IC, EBGM).

**Does not support**

- Causality.
- Incidence or absolute risk.
- Comparative clinical risk between drugs.

**Typical basis**: whole-database background comparison, single metric, no comparator restriction.

---

## Tier 2 — Comparative / characterization-level evidence

**Supports**

- Under a restricted (active-comparator) frame, one drug yields a stronger or weaker reporting signal than another.
- A subgroup, seriousness, or time-to-onset pattern is observable **within the reporting data**.

**Does not support**

- True biological susceptibility differences.
- Treatment-effect differences.
- Regulatory action thresholds.

**Typical basis**: active-comparator restriction, adjusted ROR, within-class head-to-head, demographic stratification.

---

## Tier 3 — Robustness-level evidence

**Supports**

- The signal survives alternate filters, alternate metrics, alternate comparators, or stricter exposure definitions.
- The main finding is less likely to be an artifact of one analytic choice.

**Does not support**

- External clinical validation.
- Mechanistic confirmation.

**Typical basis**: multi-metric confirmation, role-code sensitivity, alternate comparator swap, HCP-only restriction.

---

## Tier 4 — Excluded inference zone

Outside the evidence ceiling of any FAERS-only design unless external data are explicitly added:

- Definitive causal claims.
- Clinical incidence or absolute-risk claims.
- Benefit–risk recommendations.
- Regulatory or prescribing conclusions.

If a user asks for a Tier-4 statement, respond with what the design *can* support and name the external evidence that would be required (cohort study, RCT safety data, registry linkage).

---

## Required output behaviour

Every `ct-safety` report — signal-detection or comparative — must:

1. **Label each major result with its tier** (`[Tier 1]`, `[Tier 2]`, `[Tier 3]`).
2. State what the strongest validation layer actually proves.
3. State what remains unvalidated.
4. State which claims are forbidden *because their dependencies are absent* (e.g. "no incidence claim: FAERS has no denominator population").

### Suggested report block

```markdown
## Evidence Statement

| Finding | Tier | Supports | Does NOT support |
|---|---|---|---|
| ROR 3.2 (2.1–4.9) for drug A vs background | 1 | Disproportionate reporting | Incidence, causality |
| aROR 1.8 (1.2–2.7) for drug A vs comparator B | 2 | Relative reporting difference under shared indication | Treatment-effect difference |
| Direction stable across ROR / IC / EBGM and PS+SS | 3 | Not an artifact of one analytic choice | External clinical validation |

**Forbidden claims for this design**: incidence, absolute risk, causal attribution, prescribing recommendation.
```

---

## Dependency consistency (why tiers cannot be skipped)

A tier can only be claimed if the corresponding module actually ran in the executed configuration:

| Claimed tier | Prerequisite module that must be present |
|---|---|
| Tier 2 | An explicitly declared comparator restriction or class comparison |
| Tier 2 (subgroup / onset) | The subgroup or onset field must be declared available and non-sparse |
| Tier 3 | At least one alternate filter, metric, or comparator actually executed |

**Self-check before final output**

- Does any conclusion require a comparator, subgroup field, or onset variable that was never declared?
- Does the Minimal Executable version claim a tier that only Advanced / Publication+ modules can support?
- Is any Tier-1 result being phrased in Tier-2 or Tier-4 language ("increases risk", "causes", "should avoid")?

Any "yes" → revise the wording before output.

---

## Language guardrails

| Do not write | Write instead |
|---|---|
| "Drug A increases the risk of X" | "Drug A is disproportionately reported with X [Tier 1]" |
| "Drug A is safer than drug B" | "Under active-comparator restriction, drug A shows a lower reporting odds for X than drug B [Tier 2]" |
| "The incidence of X was 3%" | "X accounted for 3% of reports for drug A; FAERS cannot estimate incidence" |
| "Clinicians should prefer B" | "This design cannot support prescribing recommendations (Tier 4)" |
