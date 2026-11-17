## Description:

企服助手一键初始化技能，当新用户输入初始化或安装触发词时，自动检测并安装8个核心依赖技能，然后引导用户配置项目知识库。

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to bootstrap an enterprise service assistant by installing eight related helper skills and then setting up a project knowledge file with local business data and webhook configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs multiple mutable dependency skills.

Mitigation: Review the exact eight dependency skills before installing and prefer pinned versions from verified publishers.

Risk: The setup flow asks users to place a webhook secret in a regular project knowledge file.

Mitigation: Use a secret manager, environment variable, or untracked local secret file instead of storing a real webhook URL in PROJECT_KB.md.

Risk: The included shell scripts are described by security evidence as needing repair and review before trust.

Mitigation: Treat the shell scripts as untrusted until they are repaired, reviewed, and tested in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/enterprise-service-starter)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides installation of dependent skills and project knowledge configuration.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
