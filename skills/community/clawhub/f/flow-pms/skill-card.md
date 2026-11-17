## Description:

Interact with FlowDeck Project Management API (projects, cycles, tasks) for CRUD and archive/unarchive operations via the FlowDeck REST API through Supabase Edge Functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[araujodgdev](https://clawhub.ai/user/araujodgdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to inspect FlowDeck project status, cycle progress, tasks, comments, and to perform project-management mutations through the FlowDeck REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a bearer API key for broad remote FlowDeck changes.

Mitigation: Use a scoped, revocable API key stored in the protected FLOWBOARD_API_KEY environment variable.

Risk: The API key can be sent to a configurable base URL.

Mitigation: Do not set FLOWBOARD_BASE_URL or --base-url to untrusted hosts; use only the expected FlowDeck API gateway.

Risk: Create, update, archive, unarchive, and delete actions can change remote project-management records.

Mitigation: Require explicit confirmation before any mutation and verify the target resource is unambiguous.

## Reference(s):

- [FlowBoard API Summary](references/openapi-summary.md)
- [Practical Workflows in PT-BR](references/workflows-ptbr.md)
- [ClawHub Skill Page](https://clawhub.ai/araujodgdev/skills/flow-pms)
- [Publisher Profile](https://clawhub.ai/user/araujodgdev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or mutate remote FlowDeck project-management records when supplied with a bearer API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
