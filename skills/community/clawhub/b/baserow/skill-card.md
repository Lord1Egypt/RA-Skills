## Description:

Work with Baserow tables/rows over the REST API for reads, inserts, and updates. Use when user asks to view or modify Baserow CRM/pipeline data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericjbone](https://clawhub.ai/user/ericjbone)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect and update Baserow-backed CRM or pipeline tables through REST API reads, inserts, and updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill artifact exposes a live-looking static Baserow API token.

Mitigation: Revoke and rotate the token, remove it from the skill and package history, and replace examples with placeholders before use.

Risk: The skill describes reading or sourcing a shared credential file, which can disclose secrets or load unintended values.

Mitigation: Avoid printing or sourcing shared credential files; load secrets through a controlled environment or secret manager.

Risk: POST and PATCH examples can modify live CRM rows that are treated as source-of-truth data.

Mitigation: Require explicit confirmation of table, row, and changed fields before writes, and prefer small scoped updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericjbone/skills/baserow)
- [Baserow API documentation for database 265](https://baserow.ericbone.me/api-docs/database/265)
- [Baserow instance](https://baserow.ericbone.me)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, curl, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus BASEROW_BASE_URL and BASEROW_TOKEN environment variables; write examples may modify live Baserow rows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
