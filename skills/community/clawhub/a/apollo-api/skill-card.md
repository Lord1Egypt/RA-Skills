## Description:

Helps agents search and enrich Apollo.io people and companies and manage sales contacts and accounts through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and developers use this skill to prospect, enrich leads, manage Apollo contacts and accounts, and set up approved sales workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Apollo may grant broader access than the task needs.

Mitigation: Review OAuth scopes and prefer read-only access where possible.

Risk: Contact changes or sequence actions may affect live sales records and outreach.

Mitigation: Confirm each write or sequence action with the user before execution.

Risk: Enrichment results and trigger destinations may expose personal or business data.

Mitigation: Return only necessary fields and verify destinations before sending data.

## Reference(s):

- [Apollo API documentation](https://docs.apollo.io/reference)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Apollo skill release](https://clawhub.ai/byungkyu/skills/apollo-api)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with commands, code snippets, and concise API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API results may contain personal or business data; return only fields needed for the task.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
