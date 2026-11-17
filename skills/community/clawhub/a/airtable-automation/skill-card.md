## Description:

Automate Airtable tasks via Rube MCP (Composio): records, bases, tables, fields, views. Always search tools first for current schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sohamganatra](https://clawhub.ai/user/sohamganatra)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to guide agents through Airtable record, schema, comment, and search workflows using Rube MCP and Composio's Airtable toolkit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables record updates, schema changes, deletes, and bulk deletes on connected Airtable bases without built-in preview safeguards.

Mitigation: Require the agent to show the target base, table, records, and affected count, then obtain explicit approval before updates, schema changes, deletes, or bulk deletes.

Risk: Using the skill gives the connected Airtable account automation access through Rube MCP.

Mitigation: Use an Airtable account whose permissions match the intended scope, and avoid connecting accounts with broader access than the workflow needs.

## Reference(s):

- [Rube MCP](https://rube.app/mcp)
- [ClawHub skill page](https://clawhub.ai/sohamganatra/skills/airtable-automation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with ordered tool sequences and parameter notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP connection prerequisites, Airtable tool slugs, formula examples, pagination notes, and batch-limit cautions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
