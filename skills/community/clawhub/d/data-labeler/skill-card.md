## Description: <br>
Data Labeler is a local command-line utility for logging, searching, summarizing, and exporting data-processing activity records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data-pipeline operators use this skill to record local notes about ingest, transform, query, validation, and related data workflow steps, then inspect recent activity or export accumulated logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact is branded as Label Studio in some metadata, but the security evidence describes it as a lightweight local CLI log tracker rather than the Label Studio annotation product. <br>
Mitigation: Confirm the intended product identity before installation and use it only when a local command-line activity logger is expected. <br>
Risk: User-entered data is stored locally and can later be searched or exported. <br>
Mitigation: Do not enter secrets, customer data, or regulated information unless local storage under ~/.local/share/data-labeler and later export are acceptable. <br>
Risk: The installation or invocation path for the data-labeler command is not established by the artifact evidence. <br>
Mitigation: Verify how the command is installed or invoked before relying on it in an automation workflow. <br>


## Reference(s): <br>
- [Data Labeler ClawHub Release](https://clawhub.ai/xueyetianya/data-labeler) <br>
- [Publisher Profile](https://clawhub.ai/user/xueyetianya) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files, Configuration] <br>
**Output Format:** [Command-line text with local log and export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores user-entered records under ~/.local/share/data-labeler and can export JSON, CSV, or plain text files.] <br>

## Skill Version(s): <br>
2.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
