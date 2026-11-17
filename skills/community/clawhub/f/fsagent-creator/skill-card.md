## Description:

快速创建、删除和管理飞书机器人，支持配置 Feishu App ID、App Secret 和模型，并更新 OpenClaw agent 目录与配置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[1054570699](https://clawhub.ai/user/1054570699)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to create, list, and delete Feishu-backed agent instances, update OpenClaw configuration, and prepare the required workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unsafe admin scripts that can expose Feishu secrets.

Mitigation: Use only in a controlled OpenClaw admin environment and avoid passing real Feishu secrets directly on the command line.

Risk: The security review reports that delete behavior can remove unintended directories if agent-id handling is not validated.

Mitigation: Validate or patch agent-id handling before using deletion, and keep operator confirmation enabled.

Risk: The security review reports command-injection exposure from untrusted agent names or descriptions.

Mitigation: Avoid untrusted text in agent names and descriptions until the scripts escape and validate inputs safely.

Risk: The security review reports that new agents are silently bound to a fixed Feishu group.

Mitigation: Remove or parameterize the hard-coded Feishu group binding before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1054570699/skills/fsagent-creator)

## Skill Output:

**Output Type(s):** [shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash commands and script-generated OpenClaw configuration and workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenClaw admin environment, Feishu application credentials, and a gateway restart after create or delete actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
