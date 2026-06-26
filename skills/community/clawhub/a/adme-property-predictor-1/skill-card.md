## Description: <br>
Analyze data with `adme-property-predictor` using a reproducible workflow, explicit validation, and structured outputs for review-ready interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and cheminformatics users use this skill to estimate small-molecule ADME properties, drug-likeness, and candidate prioritization outputs from SMILES strings or CSV files. It is suited for local, reviewable early-stage analysis, not experimental or regulatory evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ADME predictions may be mistaken for experimental or regulatory-grade evidence. <br>
Mitigation: Use the outputs only for early prioritization, compare against experimental data where available, and document assumptions and model limitations before decisions. <br>
Risk: Invalid, unsupported, or out-of-domain molecular inputs can produce errors or unreliable estimates. <br>
Mitigation: Validate and canonicalize SMILES or CSV input before execution, check the molecule against the documented small-molecule scope, and stop when required inputs are missing. <br>
Risk: Unpinned local dependencies can affect reproducibility or installation reliability. <br>
Mitigation: Run in a virtual environment and pin or review dependencies, especially RDKit, before using results in a repeatable workflow. <br>


## Reference(s): <br>
- [Runtime Checklist](references/runtime_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; script output can be JSON or table-formatted text and may be written to a JSON file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires valid SMILES strings or CSV files with SMILES data; outputs are rough local estimates intended for review and prioritization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
