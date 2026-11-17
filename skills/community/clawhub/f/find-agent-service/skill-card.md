## Description:

Given a task an AI agent needs to perform, this skill finds a suitable agent-native service from the awesome-agent-native-services catalog and explains how the agent can start using it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoruilee](https://clawhub.ai/user/haoruilee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to choose an agent-native service for a requested task and return the most actionable onboarding path, such as URL onboarding, MCP configuration, SDK setup, or shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may follow mutable remote onboarding files or register with services before a human reviews the service.

Mitigation: Review each recommended service and its remote onboarding instructions manually; require approval before registration or POST requests.

Risk: Recommended npx or MCP package commands may execute unpinned packages.

Mitigation: Pin or sandbox any npx or MCP package before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haoruilee/skills/find-agent-service)
- [awesome-agent-native-services catalog](https://github.com/haoruilee/awesome-agent-native-services)
- [Moltbook URL onboarding skill](https://www.moltbook.com/skill.md)
- [Ensue documentation](https://ensue.dev/docs)
- [autoresearch@home collaboration instructions](https://raw.githubusercontent.com/mutable-state-inc/autoresearch-at-home/master/collab.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline URLs, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remote onboarding instructions, MCP configuration, SDK install commands, relevant catalog use cases, or closest-fit alternatives.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
