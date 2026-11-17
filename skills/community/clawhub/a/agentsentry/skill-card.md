## Description:

Install and configure the security-related plugins required by OpenClaw, including the `agent-sentry` plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install the agent-sentry plugin, generate an activation link, and complete plugin configuration after authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer sends a machine-derived fingerprint to the AgentSentry service and communicates with remote authentication APIs.

Mitigation: Install only after confirming trust in the publisher and reviewing the documented data collection and HTTPS authentication flow.

Risk: The installer installs the latest registry version of the plugin and grants conversation access to that plugin.

Mitigation: Prefer a version-pinned installer and review plugin permissions before use in sensitive OpenClaw environments.

Risk: Activation data and logs are stored locally during setup.

Mitigation: Review local file permissions, avoid sharing logs that may contain activation details, and clean up setup state according to organizational policy.

## Reference(s):

- [ClawHub AgentSentry listing](https://clawhub.ai/volcengine-skills/skills/agentsentry)
- [Volcengine website](https://www.volcengine.com/)
- [Volcengine skills publisher profile](https://clawhub.ai/user/volcengine-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and activation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an activation URL, local state file references, and status messages for the two-phase setup flow.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
