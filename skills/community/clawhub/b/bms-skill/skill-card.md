## Description:

Parse automotive BMS BLF CAN logs with DBC files to extract time series data for specified signals in CSV, JSON, or text formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muqiong](https://clawhub.ai/user/muqiong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automotive engineers use this skill to inspect Battery Management System CAN logs, extract named signals from BLF recordings with DBC definitions, and prepare time series outputs for analysis or visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically install Python dependencies.

Mitigation: Review dependencies first, then install trusted pinned packages in a virtual environment.

Risk: Parsing untrusted BLF, DBC, or JSON inputs and exporting data can expose the local environment to unsafe files or misleading results.

Mitigation: Use trusted input files, validate signal names against the DBC, and review extracted data before relying on it.

Risk: The plotting and extraction utilities can write generated files to caller-controlled paths.

Mitigation: Always provide explicit safe output paths and avoid writing into sensitive directories.

## Reference(s):

- [BMS CAN Analyzer on ClawHub](https://clawhub.ai/muqiong/skills/bms-skill)
- [Publisher profile](https://clawhub.ai/user/muqiong)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; analyzer outputs may be CSV, JSON, text, or PNG plots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied BLF logs, DBC definitions, signal names, and explicit output paths for generated files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
