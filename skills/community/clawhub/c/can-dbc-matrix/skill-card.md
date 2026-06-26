## Description: <br>
Parse and analyze CAN DBC matrix JSON files exported by canmatrix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankie-zeng](https://clawhub.ai/user/frankie-zeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect canmatrix-exported CAN database JSON, find messages and signals, decode raw CAN frames, and summarize ECU transmitter or receiver relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional canmatrix installation and conversion commands may introduce normal third-party package and CLI execution risk. <br>
Mitigation: Review the package source and commands before running them in the target environment. <br>
Risk: DBC and CAN database files may contain proprietary vehicle or product details. <br>
Mitigation: Avoid sharing sensitive CAN database content outside approved environments. <br>


## Reference(s): <br>
- [Canmatrix JSON Schema Reference](json-schema.md) <br>
- [ClawHub release page](https://clawhub.ai/frankie-zeng/can-dbc-matrix) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on JSON structures exported by canmatrix with --jsonExportAll.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
