## Description: <br>
Browse Airtable bases and tables, inspect records, create records, and manage fields, comments, and table actions via the Airtable API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Airtable users and automation builders use this skill to browse bases and tables, inspect records, and perform record, field, comment, and table operations through a connected Airtable account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects a third-party ClawLink plugin to the user's Airtable account through OAuth. <br>
Mitigation: Install only the intended ClawLink plugin and connect Airtable through the documented dashboard flow before using Airtable tools. <br>
Risk: Write or delete operations can modify Airtable bases, tables, records, fields, or comments. <br>
Mitigation: Approve write and delete calls only after checking the base, table, record, and intended change; use previews and explicit confirmation before execution. <br>
Risk: Record deletion is permanent and cannot be undone. <br>
Mitigation: Confirm destructive requests carefully and prefer read or preview steps before any delete operation. <br>


## Reference(s): <br>
- [Airtable API Documentation](https://airtable.com/developers/web/api/introduction) <br>
- [Airtable Base Schema](https://airtable.com/developers/web/api/schema) <br>
- [Airtable Records](https://airtable.com/developers/web/api/records) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/airtable-records) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Airtable account through ClawLink OAuth; write and delete actions should be previewed and confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
