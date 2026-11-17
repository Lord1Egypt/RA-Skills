## Description:

Guides agents in managing Basecamp projects, to-dos, messages, schedules, and documents through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Team members and developers use this skill to retrieve and manage Basecamp projects, tasks, and collaboration content. With explicit approval, they can also set up functions and scheduled or external-event automations that act on their Basecamp connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an account or changing and deleting Basecamp content could expose or alter business data.

Mitigation: Use the intended account and narrowest available permissions; confirm new connections and each write or deletion with the user.

Risk: Hosted functions and triggers can keep running and forward event data after setup.

Mitigation: Review each function and destination with the user, limit them to the task, and remove unneeded automations.

Risk: Exposed API keys could permit unauthorized access.

Mitigation: Prefer OAuth through the CLI and avoid printing, storing, or sharing API keys.

## Reference(s):

- [ClawHub Basecamp skill release](https://clawhub.ai/byungkyu/skills/basecamp)
- [Maton homepage](https://maton.ai)
- [Basecamp 4 API documentation](https://github.com/basecamp/bc3-api)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Scheduled trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Guidance]

**Output Format:** [Markdown with command and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require an authorized connection; writes and new connections require user confirmation.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
