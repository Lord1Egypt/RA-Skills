## Description: <br>
Installs and configures OpenClaw security-related plugins, including ai-assistant-security-openclaw, and guides login and setup verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install the AI Assistant Security plugin, obtain the authorization login URL, complete account linking, and verify that the security plugin is enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow performs account linking and device fingerprint transmission. <br>
Mitigation: Install only when the publisher and Volcengine/Omni Shield service are trusted, and review the authorization page before continuing. <br>
Risk: The installer stores local login state and writes a polling log. <br>
Mitigation: Review and remove .state/login_state.json and poll_login.log after setup if they are no longer needed. <br>
Risk: The installer can automatically change OpenClaw plugin configuration and restart the OpenClaw gateway. <br>
Mitigation: Run it only in the intended OpenClaw environment and inspect plugin configuration after installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-security-clawsentry) <br>
- [Volcengine official site](https://www.volcengine.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and login URL text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local setup state and polling logs during installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
