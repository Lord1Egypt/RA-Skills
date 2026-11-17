## Description:

Disease CEA Auto designs Markov or decision-tree pharmacoeconomic evaluations for a specified disease, searches for current treatments and model parameters, calculates ICER and NMB using China's latest GDP-per-capita WTP threshold, and outputs runnable Python plus a bilingual scientific report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tlb1201](https://clawhub.ai/user/tlb1201)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, health economics analysts, and policy researchers use this skill to draft China-centered, bilingual cost-effectiveness comparisons across treatments for a specified disease. It is suited for generating candidate models, code, and reports that require source verification before clinical, policy, or purchasing use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs depend on live web sources, treatment choices, cost data, and modeling assumptions that may be incomplete, outdated, or jurisdiction-specific.

Mitigation: Verify citations, drug costs, clinical guidelines, GDP threshold values, and all assumptions against authoritative sources before relying on results.

Risk: Generated cost-effectiveness conclusions could be misused for clinical, policy, or purchasing decisions without domain review.

Mitigation: Require review by qualified health economics and clinical stakeholders, and inspect sensitivity analyses before applying conclusions.

## Reference(s):

- [Model Parameter Reference Guide](artifact/references/model_params.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Bilingual Markdown report with Python code, CEA tables, and optional generated chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include web-cited treatment parameters, ICER/NMB rankings, one-way sensitivity analysis, and Python-generated cost-effectiveness plane and NMB bar chart outputs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
