## Description:

Set up and troubleshoot Feishu or Lark messaging integration with Hermes Agent, including connection checks, access control, and common failure modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuxuclassmate](https://clawhub.ai/user/xuxuclassmate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect Hermes Agent to Feishu or Lark and diagnose bot response, permission, gateway, and configuration failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting can expose Feishu/Lark app secrets, encryption keys, verification tokens, or gateway logs to the local agent.

Mitigation: Use production allowlists, avoid sharing logs that contain sensitive values, and keep secrets out of committed files.

Risk: Restarting the Hermes gateway applies configuration changes and can interrupt message handling.

Mitigation: Restart the gateway only when configuration changes are intentional and expected.

Risk: Broad user access settings can allow unintended Feishu or Lark users to interact with the gateway.

Mitigation: Prefer explicit allowed-user settings over allow-all settings for production deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuxuclassmate/skills/feishu-setup-troubleshooting)
- [Publisher profile](https://clawhub.ai/user/xuxuclassmate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the hermes CLI and Feishu/Lark environment configuration.]

## Skill Version(s):

1.2.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
