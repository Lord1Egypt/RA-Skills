## Description:

Use the Dopost REST API to publish, schedule, upload media for, and manage social media posts programmatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dopost](https://clawhub.ai/user/dopost)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, social media operators, and external automation users use this skill to work with Dopost accounts, posts, schedules, media uploads, and publishing status from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent using this skill can publish, schedule, reschedule, upload media for, or delete social content through a Dopost account.

Mitigation: Require explicit user confirmation after showing the target account, post or media ID, content, platform options, and scheduled time before making write or delete requests.

Risk: The skill depends on DOPOST_API_KEY for authenticated API access.

Mitigation: Provide DOPOST_API_KEY through a scoped environment variable or secret manager and avoid giving the agent broad access to general .env files.

## Reference(s):

- [Dopost API documentation](https://dopost.co/docs/api)
- [ClawHub skill page](https://clawhub.ai/dopost/skills/dopost)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce authenticated Dopost API request examples and workflow guidance for publishing, scheduling, media upload, status checks, and deletion.]

## Skill Version(s):

1.1.0 (source: openclaw metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
