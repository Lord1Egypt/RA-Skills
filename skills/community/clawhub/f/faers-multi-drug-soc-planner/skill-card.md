## Description:

Generates complete FAERS-based multi-drug single-SOC safety comparison research designs from a user-provided drug set, comparator, and adverse event domain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanruoyu](https://clawhub.ai/user/shanruoyu)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, pharmacovigilance analysts, and developers use this skill to design FAERS or OpenFDA comparative safety studies for multiple drugs within one System Organ Class or bounded adverse-event domain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated FAERS study plans could be mistaken for medical advice or causal proof.

Mitigation: Review outputs as research-design guidance only, and preserve FAERS limitations that distinguish disproportionality from incidence or causal risk.

Risk: Comparator choice, sparse indication fields, or data-quality assumptions can weaken a pharmacovigilance design.

Mitigation: Have a qualified reviewer check comparator suitability, indication completeness, drug normalization, case-count thresholds, and robustness plans before analysis.

## Reference(s):

- [FDA FAERS Public Dashboard](https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown research plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces four workload configurations, a recommended primary plan, workflow steps, figure and table plans, validation strategy, minimal executable path, publication upgrade path, and risk review.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
