## Description: <br>
Baserow helps an agent create, read, update, and delete rows, list tables and fields, inspect table structure, and support database workflows through the Baserow CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzakirov](https://clawhub.ai/user/jzakirov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill when they need an agent to inspect Baserow schemas, query records, create or update rows, and run batch row operations through the Baserow CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read or modify Baserow data using configured credentials. <br>
Mitigation: Use the narrowest practical Baserow token and confirm the target workspace, database, table, and row data before execution. <br>
Risk: Delete and batch-delete commands are destructive. <br>
Mitigation: Require explicit user approval before destructive commands and use the documented confirmation flag only after review. <br>
Risk: The skill depends on the external baserow-cli package. <br>
Mitigation: Verify the package source and version before installation or update. <br>


## Reference(s): <br>
- [Baserow](https://baserow.io) <br>
- [ClawHub release page](https://clawhub.ai/jzakirov/baserow-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Baserow CLI JSON output and environment-based configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
