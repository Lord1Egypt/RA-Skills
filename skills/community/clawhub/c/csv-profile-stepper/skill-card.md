## Description: <br>
A command-line skill for CSV profiling that should be reviewed carefully because security evidence reports undisclosed caller-directed network transfer options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[askjda](https://clawhub.ai/user/askjda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners can use this skill to attempt quick CSV profiling from the command line, with results written to standard output and JSON or TXT files. Use only with non-sensitive local files until the reported network-transfer behavior is removed or documented. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports undisclosed options that can upload local file contents to a caller-selected endpoint. <br>
Mitigation: Do not use --endpoint and --payload with sensitive files; inspect and remove or document network-transfer behavior before deployment. <br>
Risk: Security evidence reports that the implementation may not compute the promised CSV profile. <br>
Mitigation: Validate outputs on benign test CSV files and require implementation changes before relying on profiling results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/askjda/csv-profile-stepper) <br>
- [Publisher profile](https://clawhub.ai/user/askjda) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown instructions with command-line examples; runtime output is JSON or TXT.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output files and may print status or profile data to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
