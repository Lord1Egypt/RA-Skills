## Description:

Creates multiple independent Feishu bot configurations for OpenClaw, including per-bot memory, workspace, model, personality, and Feishu credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lcz5221-svg](https://clawhub.ai/user/lcz5221-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up batches of isolated Feishu bots in OpenClaw with separate workspaces, memory files, route bindings, model settings, and Feishu app credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflow modifies persistent OpenClaw configuration and creates files under per-agent workspaces.

Mitigation: Back up ~/.openclaw/openclaw.json and review generated account, agent, binding, and workspace files before restarting the gateway.

Risk: The security evidence reports unsafe default access policies for shared or production Feishu use.

Mitigation: Change generated bot policies to allowlist access and mention-required behavior before use outside a trusted test environment.

Risk: The security evidence reports a command-injection risk if untrusted agentId values reach the setup script.

Mitigation: Run the script only with trusted configuration files and manually review bot identifiers before execution.

Risk: Feishu app secrets and tokens appear in the input and generated configuration.

Mitigation: Store configuration files securely, limit file access, and rotate secrets if they are exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lcz5221-svg/skills/feishu-duoge002)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify persistent OpenClaw configuration and create per-bot workspace files when its setup script is run.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
