## Description: <br>
Gateway Guardian helps OpenClaw users monitor gateway configuration, roll back invalid changes, recover crashed gateway services, and send Feishu, Telegram, or Discord notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dios-man](https://clawhub.ai/user/dios-man) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to install, check, configure, or remove a background gateway guardian. It is intended to protect openclaw.json, restart the gateway after repeated failures, and notify the operator when recovery succeeds or needs manual attention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent user-level services that can modify OpenClaw configuration and restart the gateway. <br>
Mitigation: Install only when background recovery automation is intended, and review service registration and recovery behavior before enabling it. <br>
Risk: Recovery alerts may include logs or operational details. <br>
Mitigation: Review notification destinations before forwarding alerts, and restrict group notifications to trusted channels. <br>
Risk: Installation and recovery depend on packaged scripts, downloaded files when local files are absent, and guardian.conf values. <br>
Mitigation: Prefer reviewed packaged files or pinned downloads, verify script sources, and safely quote or validate configuration values before persistent changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dios-man/gateway-config-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that create user-level systemd services, OpenClaw config backups, and notification settings.] <br>

## Skill Version(s): <br>
1.6.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
