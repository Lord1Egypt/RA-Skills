## Description: <br>
ClawSentry installs and configures the security-related OpenClaw plugins, including claw-sentry, through a two-phase activation and configuration flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install the claw-sentry security plugin, generate an activation link, and finalize plugin configuration after platform authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enrolls the OpenClaw host with an external authorization service and sends a device fingerprint. <br>
Mitigation: Install only when the ClawSentry/Volcengine service is trusted, and run setup first in a controlled environment. <br>
Risk: Activation state, login tokens, device fingerprint data, and logs are persisted locally under .state during setup. <br>
Mitigation: Inspect and remove local login state files and logs after activation if they are no longer needed. <br>
Risk: The installer can install or replace the claw-sentry plugin, write API-key configuration, allow plugin conversation access, and restart the OpenClaw gateway. <br>
Mitigation: Review the configuration changes and run the installer with appropriate operational approval on a non-critical host first. <br>


## Reference(s): <br>
- [ClawSentry ClawHub page](https://clawhub.ai/volcengine-skills/clawsentry) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal output with shell commands and activation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a bundled Node.js installer that writes local activation state and OpenClaw plugin configuration.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
