## Description:

Helps agents use Attio to find and manage CRM records, tasks, notes, lists, and meetings through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to query and update Attio CRM data, and, with separate approval, automate Attio actions using scheduled or connected-app events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access to the wrong Attio workspace or broader CRM data than intended.

Mitigation: Confirm the Attio account and connection before use, and authorize only the access needed for the task.

Risk: Incorrect writes or deletions may change CRM records.

Mitigation: Start with read-only queries and obtain explicit user approval before each write or delete.

Risk: Triggers and destinations may continue acting on or forwarding data without further interaction.

Mitigation: Review the action, schedule, and destination before enabling automation; disable or remove it when no longer needed.

## Reference(s):

- [Attio skill on ClawHub](https://clawhub.ai/byungkyu/skills/attio-api)
- [Maton](https://maton.ai)
- [Attio REST API overview](https://docs.attio.com/rest-api/overview)
- [Attio REST API endpoint reference](https://docs.attio.com/rest-api/endpoint-reference)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Attio API responses and instructions for user-approved CRM changes or automation.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
