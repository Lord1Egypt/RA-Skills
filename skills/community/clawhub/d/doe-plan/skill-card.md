## Description:

Evidence-backed bioprocess DOE planning for fermentation and upstream optimization, producing traceable factor hypotheses, DOE designs, run sheets, and reports from patent, paper, and web evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minmin-patsnap](https://clawhub.ai/user/minmin-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and R&D scientists use this skill to turn readable bioprocess evidence into an executable DOE plan with traceable factors, design rationale, run sheets, and a final report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DOE recommendations may be unsupported when evidence coverage is thin, inputs are missing, or factor ranges are not traceable.

Mitigation: Require readable evidence, objective, responses, and hard constraints before generating a DOE recommendation; stop or label outputs as inference-heavy when coverage is insufficient.

Risk: The workflow can run local Python scripts, use optional PatSnap retrieval, and create planning artifacts in the working directory.

Mitigation: Install and run it only where local script execution and DOE output files are acceptable; use a dedicated project/output directory and review PatSnap MCP access before enabling it.

Risk: Generated bioprocess factor ranges and designs could be mistaken for validated operating conditions.

Mitigation: Review outputs before execution, preserve facts, inferences, and unknowns separately, and apply the documented regulatory and QbD guardrails before acting on the plan.

## Reference(s):

- [Bioprocess Factor Library](references/bioprocess-factor-library.md)
- [DOE Method Selector](references/doe-method-selector.md)
- [Output Contract](references/output-contract.md)
- [Evidence to Factor Mapping](references/patent-to-factor-mapping.md)
- [Regulatory and QbD Guardrails](references/regulatory-qbd-guardrails.md)
- [PatSnap Open Platform](https://open.patsnap.com)
- [Eureka Expert Edition](https://eureka.patsnap.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON, CSV, and Markdown files with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes evidence_catalog.json, factor_hypotheses.json, doe_design.json, run_sheet.csv, and doe_plan.md; requires user-supplied or fetched readable evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
