## Description:

飞书任务Bot身份 helps agents use a Feishu/Lark bot application identity with the v1 Tasks API to list tasks assigned to the bot without user login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixiang92229](https://clawhub.ai/user/lixiang92229)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent must inspect Feishu/Lark task assignments through a bot or application identity instead of a user identity. It is suited to task-status checks and bot-owned task listing workflows that rely on Feishu application credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the current artifact lists Feishu tasks but asks users to grant broader task-write authority than the shipped script needs.

Mitigation: Grant read-only task permission for this artifact where possible, avoid task-write scope unless a reviewed write-capable version is needed, and prefer pinned installation sources.

## Reference(s):

- [Bot task listing command reference](references/lark-task-bot-get-my-tasks.md)
- [Project homepage from ClawHub metadata](https://github.com/lixiang92229/feishu-bot-task)
- [ClawHub skill page](https://clawhub.ai/lixiang92229/skills/feishu-bot-task)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON task-list output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET environment variables and Feishu task permissions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
