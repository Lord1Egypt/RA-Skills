## Description:

Helps agents use a connected Clockify account to track time and manage projects, clients, tasks, and workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams with a connected Clockify account use this skill to review time entries and manage time tracking, projects, and workspace resources. With separate approval, they can automate actions using hosted functions and triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an account or modifying Clockify data can affect the user's workspace.

Mitigation: Review OAuth access and confirm every new connection and write operation before approval.

Risk: Hosted functions and triggers can run repeatedly or forward events to external destinations.

Mitigation: Review each function, trigger, and destination before approval, especially continuous runs and URL forwarding.

## Reference(s):

- [Clockify API documentation](https://docs.clockify.me/)
- [Maton](https://maton.ai)
- [Maton API documentation](https://docs.maton.ai/api-reference/overview)
- [Clockify skill release](https://clawhub.ai/byungkyu/skills/clockify)
- [Time trigger reference](artifact/references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize selected Clockify data and propose actions for user confirmation.]

## Skill Version(s):

1.2.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
