## Description:

Guides an agent through setting up a Teambition or Meego project integration, including plugin installation, DingTalk-based robotUserToken retrieval, and digital worker registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaohuifeng](https://clawhub.ai/user/gaohuifeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Teambition or Meego project automation and register a digital worker by following linked setup guidance. It is intended for agents assisting with project-management integration setup rather than performing business actions without review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on mutable external documentation and connector pages for its real behavior.

Mitigation: Review the linked instructions before use and prefer a pinned or locally packaged version of the setup steps for production workflows.

Risk: The setup flow may involve sign-in, account-like service creation, token handling, or submission of personal or business data.

Mitigation: Require explicit user confirmation before those actions and avoid exposing credentials, robotUserToken values, or sensitive project data in agent-visible logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaohuifeng/skills/ali-feishu-project)
- [tb-skills AI integration guide](https://github.com/teambition/tb-skills/blob/main/README_FOR_AI.md)
- [Meego Feishu project connector](https://clawhub.ai/wadxm/feishu-project-connector)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with external links and inline setup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require user confirmation before sign-in, token handling, account creation, or submission of personal or business data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
