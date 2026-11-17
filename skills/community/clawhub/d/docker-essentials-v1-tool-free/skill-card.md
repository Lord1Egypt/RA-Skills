## Description:

提供Docker V1经典命令集与基础容器管理,适合维护旧版Docker环境的开发者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate and review Docker V1 and docker-compose V1 commands for maintaining legacy container environments, managing images and containers, debugging services, and preparing migration assessments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can suggest destructive Docker operations such as remove, prune, or down -v.

Mitigation: Require explicit user approval before destructive commands and back up important containers, images, and volumes first.

Risk: The skill may guide registry login, push, or rebuild workflows that can expose credentials or publish unintended images.

Mitigation: Do not paste passwords or tokens into commands or logs, and review registry targets and image tags before execution.

Risk: The skill focuses on legacy Docker V1 and docker-compose V1 environments.

Mitigation: Use it only when legacy Docker support is required and keep the agent scoped to that maintenance or migration task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/docker-essentials-v1-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, YAML, and Dockerfile code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Docker commands that require user review before execution.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
