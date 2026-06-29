## Description: <br>
Assist with installing, configuring, and using the Apple Mail channel plugin for OpenClaw/Hermes on macOS to monitor and respond to emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jehadurre](https://clawhub.ai/user/jehadurre) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to set up the @jehadurre/openclaw-apple-mail channel on macOS, including installation, configuration examples, and troubleshooting for email monitoring and replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The related plugin can access Apple Mail and may process private, business, or customer email if configured too broadly. <br>
Mitigation: Install only when Apple Mail access is intended, use a narrow sender allowlist, avoid allowFrom ["*"] except on dedicated low-risk accounts, and keep archiveOnReply disabled until the setup is tested. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jehadurre/apple-mail-setup) <br>
- [Apple Mail Plugin Package](https://www.npmjs.com/package/@jehadurre/openclaw-apple-mail) <br>
- [Apple Mail Plugin Documentation](https://openclaw-apple-mail.jehadurre.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focused on macOS Apple Mail, OpenClaw or Hermes setup, and plugin configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, package.json, skill.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
