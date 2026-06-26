## Description: <br>
Dream Of Clawra helps an OpenClaw agent choose hosted Haocun dancing or selfie images and send them to messaging channels such as WhatsApp or Signal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qidu](https://clawhub.ai/user/qidu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add persona-driven image selection and messaging to an OpenClaw agent. It supports requests for dancing or selfie-style images and sends a hosted image after the user provides the channel and recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send images through messaging accounts. <br>
Mitigation: Require explicit confirmation for each recipient, channel, caption, and image before sending. <br>
Risk: The installer can persistently change the agent identity and persona files. <br>
Mitigation: Back up IDENTITY.md and SOUL.md and review the installer before running it. <br>
Risk: OpenClaw gateway credentials and broad tool access can increase impact if misused. <br>
Mitigation: Keep the gateway token private and narrow allowed tools to the minimum needed for the deployment. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/qidu/dream-of-clawra) <br>
- [OpenClaw Project](https://github.com/openclaw/openclaw) <br>
- [Hosted Image Asset Source](https://cdn.jsdelivr.net/gh/christoagent/haoclaw@main/assets/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and messaging API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Selects hosted image URLs and can invoke OpenClaw messaging with channel, target, caption, and media parameters.] <br>

## Skill Version(s): <br>
1.0.8 (source: server evidence, package.json, manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
