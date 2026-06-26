## Description: <br>
Set up automatic notifications when OpenClaw gateway restarts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deemoartisan](https://clawhub.ai/user/deemoartisan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure gateway startup notifications through channels such as iMessage, WhatsApp, Telegram, Discord, or Slack. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent OpenClaw hook that sends notifications whenever the gateway starts. <br>
Mitigation: Install it only when ongoing startup notifications are wanted, and remove or disable the OpenClaw hook when automatic notifications are no longer needed. <br>
Risk: Gateway status messages sent to public or shared messaging channels can expose infrastructure activity. <br>
Mitigation: Use a private trusted channel for notification delivery and avoid public Slack or Discord destinations for infrastructure status. <br>


## Reference(s): <br>
- [Supported Channels](references/CHANNELS.md) <br>
- [Manual Setup Guide](references/MANUAL.md) <br>
- [Gateway Notify on ClawHub](https://clawhub.ai/deemoartisan/gateway-notify) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell commands and generated hook configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps for a persistent OpenClaw gateway startup notification hook.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and CHANGELOG.md, released 2026-03-09) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
