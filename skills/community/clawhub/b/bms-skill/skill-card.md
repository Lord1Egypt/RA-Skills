## Description: <br>
Parses automotive BMS BLF CAN logs with DBC files to extract and visualize signal time series data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Muqiong](https://clawhub.ai/user/Muqiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automotive engineers use this skill to extract, inspect, and visualize battery management system signal time series from BLF CAN logs using matching DBC definitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation and local parsing tools may affect the user's Python environment. <br>
Mitigation: Install dependencies from trusted sources in an isolated Python virtual environment. <br>
Risk: The scripts can write local result files or plots when output paths are provided. <br>
Mitigation: Use explicit output paths and review generated files before sharing or reusing them. <br>


## Reference(s): <br>
- [BMS CAN Analyzer on ClawHub](https://clawhub.ai/Muqiong/bms-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python-oriented workflow notes, and JSON, CSV, text, or PNG analysis outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided BLF logs, DBC definitions, and exact signal names; output files are written only when an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
