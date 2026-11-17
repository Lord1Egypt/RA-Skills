## Description:

Install and configure the security-related plugins required by OpenClaw, including the `ai-assistant-security-openclaw` plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinjianfenghzau-wq](https://clawhub.ai/user/qinjianfenghzau-wq)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to install and prepare the ai-assistant-security-openclaw plugin, generate a login authorization link, and enable the plugin configuration after login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled installer modifies OpenClaw plugin configuration and installs an unpinned plugin package.

Mitigation: Run only after publisher review, prefer a pinned installer, and verify OpenClaw configuration changes before and after execution.

Risk: The installer sends a device fingerprint to the ClawSentry service during login token creation and login polling.

Mitigation: Review the data flow and privacy expectations before use, especially on shared, regulated, or production machines.

Risk: Login tokens, device fingerprints, and authentication-related material may be stored in local state files or logs.

Mitigation: Use restrictive file permissions, redact logs before sharing, and prefer OS secret storage or another protected credential store.

Risk: The bundled script uses shell command execution while handling plugin configuration.

Mitigation: Inspect the script before running it and prefer a reviewed implementation that avoids shell-string command execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qinjianfenghzau-wq/skills/clawprepub)
- [ClawHub Publisher Profile](https://clawhub.ai/user/qinjianfenghzau-wq)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Volcengine Product Site](https://www.volcengine.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and login URL text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a login URL and installation status guidance after running the bundled installer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
