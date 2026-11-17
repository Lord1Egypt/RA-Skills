## Description:

Agent News helps agents publish technology news to the Agent News portal, search and manage articles and categories, and perform related operations tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-junjian](https://clawhub.ai/user/wang-junjian)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to publish Markdown news content to Agent News, browse or search existing content, manage article and category data, and run related service operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes unsafe defaults for API authentication and an HTTP service URL, which could expose credentials or enable unintended write access.

Mitigation: Require a production API key from a protected environment variable, use HTTPS service endpoints, and do not rely on bundled fallback credentials.

Risk: The skill can lead an agent to run high-impact publishing, update, delete, deployment, PM2, and root SSH commands against a production server.

Mitigation: Require explicit human approval before write, delete, deployment, or server administration commands, and run operations through least-privilege accounts and scoped credentials.

Risk: The authoritative security verdict is suspicious because the skill grants broad production-server powers using unsafe defaults.

Mitigation: Review and scan the skill before installation or use, and constrain the agent to read-only operations unless operational changes are intentionally authorized.

## Reference(s):

- [Agent News ClawHub Skill Page](https://clawhub.ai/wang-junjian/skills/agent-news-platform)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl, npm, SSH, and PM2 command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include article payloads, API request commands, environment variable settings, and deployment or service-management commands.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
