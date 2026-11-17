## Description:

Generates complete FAERS-based multi-drug single-SOC safety comparison research designs from a user-provided drug set, comparator, and adverse event domain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, developers, and pharmacovigilance analysts use this skill to plan comparative FAERS or OpenFDA safety-signal studies across multiple drugs within one MedDRA System Organ Class or bounded adverse-event domain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated FAERS study plans could be mistaken for clinical advice or causal safety conclusions.

Mitigation: Treat outputs as medical research planning aids only, and review for non-causal wording before using them in publications or decisions.

Risk: Study plans may depend on comparator suitability and known FAERS limitations such as reporting bias, sparse indications, and non-incidence disproportionality signals.

Mitigation: Review comparator choice, require explicit FAERS limitations, and confirm that results are framed as reporting disproportionality rather than incidence or causal risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/faers-multi-drug-soc-planner-1)
- [AIpoch publisher profile](https://clawhub.ai/user/aipoch-ai)
- [FDA FAERS public dashboard and downloads](https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research plan with comparison tables and workflow sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Always produces four workload configurations, a recommended primary plan, validation strategy, risk review, minimal executable version, and publication upgrade path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
