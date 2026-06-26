## Description: <br>
Work with Baserow tables/rows over the REST API for reads, inserts, and updates. Use when user asks to view or modify Baserow CRM/pipeline data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericjbone](https://clawhub.ai/user/ericjbone) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to read, insert, and update Baserow CRM or pipeline records through the REST API. It is intended for workflows that need table-specific guidance for Renpho sales pipeline data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a live-looking static API token in the skill text. <br>
Mitigation: Do not use the embedded token value; rotate it if it belongs to you and replace it with your own least-privilege Baserow token stored outside committed skill text. <br>
Risk: The skill enables authenticated writes to CRM data. <br>
Mitigation: Before any write operation, manually verify the exact table, row ID, and fields being changed. <br>
Risk: Bulk or broad updates can affect source-of-truth sales records. <br>
Mitigation: Prefer small scoped updates and echo changed fields for review. <br>


## Reference(s): <br>
- [Baserow API documentation for database 265](https://baserow.ericbone.me/api-docs/database/265) <br>
- [ClawHub skill page](https://clawhub.ai/ericjbone/baserow) <br>
- [Publisher profile](https://clawhub.ai/user/ericjbone) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash, Python, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Baserow base URL and API token supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
