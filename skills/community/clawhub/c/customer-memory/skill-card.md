## Description:

Give AI agents persistent memory of customer interactions, preferences, and history using BlueColumn for support, sales, and customer-success workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Support, sales, and customer-success agents use this skill to recall and store customer-specific interaction history, preferences, issue resolutions, and notes in BlueColumn.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent storage of identifiable customer data may create privacy, retention, and access-control exposure.

Mitigation: Define permitted data before use, redact secrets and sensitive personal data, prefer opaque customer IDs over emails, and establish retention, deletion, and access-review procedures.

Risk: Customer memory recall could mix data across tenants or customers if queries are too broad.

Mitigation: Restrict recall to the current tenant and customer and review returned sources before using recalled context in customer-facing responses.

## Reference(s):

- [BlueColumn API Reference](references/api.md)
- [BlueColumn](https://bluecolumn.ai)
- [ClawHub Skill Page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/customer-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key; outputs should avoid logging or exposing customer data and credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
