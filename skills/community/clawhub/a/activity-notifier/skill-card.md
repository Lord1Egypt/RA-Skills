## Description:

Broadcast agent activity status to Discord channel (thinking, tool use, web search, coding, done, error). Use for transparency so users know agent is working.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silvermoonswk](https://clawhub.ai/user/silvermoonswk)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to send concise Discord updates while an agent is thinking, using tools, searching the web, coding, waiting, finishing, or reporting an error.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activity updates may be sent to a fixed or unintended Discord channel, exposing task context without clear user approval.

Mitigation: Configure an explicit trusted activity channel before use and keep notifications generic.

Risk: Discord notifications can accidentally reveal prompts, credentials, file contents, command output, or detailed errors.

Mitigation: Do not include sensitive data in activity messages; limit updates to brief status and progress summaries.

## Reference(s):

- [Activity Notifier ClawHub listing](https://clawhub.ai/silvermoonswk/skills/activity-notifier)
- [silvermoonswk ClawHub profile](https://clawhub.ai/user/silvermoonswk)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Concise Discord activity messages, often Markdown-formatted.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Discord token and a trusted activity channel; messages should avoid sensitive task details.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
