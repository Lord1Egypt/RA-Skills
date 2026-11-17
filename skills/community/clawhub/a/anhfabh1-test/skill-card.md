## Description:

Install and configure the security-related plugins required by OpenClaw, including the `ai-assistant-security-openclaw` plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinjianfenghzau-wq](https://clawhub.ai/user/qinjianfenghzau-wq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install and prepare ClawSentry security plugins for an OpenClaw environment, complete login authorization, and update local plugin configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow changes OpenClaw plugin state and restarts the OpenClaw gateway.

Mitigation: Review the installation plan before execution, run it only in an approved OpenClaw environment, and verify plugin state after completion.

Risk: The skill sends a stable machine fingerprint to vendor endpoints and stores login and credential-related data locally.

Mitigation: Use only on approved machines, protect local state and log files, and rotate or revoke credentials if local exposure is suspected.

Risk: The setup installs an unpinned external plugin and invokes local OpenClaw commands with configuration payloads.

Mitigation: Confirm the plugin source and expected configuration before installation, and avoid running the skill with unnecessary elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qinjianfenghzau-wq/skills/anhfabh1-test)
- [Volcengine](https://www.volcengine.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit a login URL and status guidance for completing OpenClaw plugin authorization.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
