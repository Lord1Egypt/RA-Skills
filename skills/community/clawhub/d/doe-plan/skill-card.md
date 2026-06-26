## Description: <br>
Evidence-backed bioprocess DOE planning for fermentation and upstream optimization that turns fetched patent, paper, and web evidence into traceable factor hypotheses, selects DOE designs, generates run sheets, and renders a DOE plan report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minmin-patsnap](https://clawhub.ai/user/minmin-patsnap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and R&D teams use this skill to convert readable patent, paper, and web evidence into traceable DOE plans for fermentation and upstream bioprocess optimization. It supports factor extraction, range proposal, design selection, run-sheet generation, and report rendering while separating facts, inferences, and unknowns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DOE recommendations can be misleading when source evidence is thin, unreadable, or insufficiently traced. <br>
Mitigation: Require readable evidence coverage before producing recommendations and label unsupported factor ranges, mechanisms, and recommendations as inferences or unknowns. <br>
Risk: Generated run sheets and experimental plans may conflict with process safety, operability, or quality constraints. <br>
Mitigation: Review objective, response metrics, constraints, operability limits, and QbD guardrails before executing a proposed experiment. <br>
Risk: Pipeline commands create or overwrite planning artifacts. <br>
Mitigation: Review command arguments and output paths before execution, preserve successful earlier-stage artifacts after failures, and use staged validation before running the full pipeline. <br>


## Reference(s): <br>
- [Bioprocess Factor Library](references/bioprocess-factor-library.md) <br>
- [DOE Method Selector](references/doe-method-selector.md) <br>
- [Output Contract](references/output-contract.md) <br>
- [Evidence to Factor Mapping](references/patent-to-factor-mapping.md) <br>
- [Regulatory and QbD Guardrails](references/regulatory-qbd-guardrails.md) <br>
- [PatSnap Open Platform](https://open.patsnap.com) <br>
- [Eureka Expert Edition](https://eureka.patsnap.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, CSV] <br>
**Output Format:** [Markdown guidance with shell commands plus generated JSON, CSV, and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces evidence_catalog.json, factor_hypotheses.json, doe_design.json, run_sheet.csv, and doe_plan.md with traceability requirements.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
