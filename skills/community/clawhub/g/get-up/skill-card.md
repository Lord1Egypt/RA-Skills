## Description: <br>
Sends semantically selected Haocun dancing or selfie image URLs through OpenClaw messaging channels in response to photo, dance, or status requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qidu](https://clawhub.ai/user/qidu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and agent builders use this skill to let an agent select fixed dance or selfie images and send them through configured messaging channels after collecting the prompt, channel, and target. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can persistently change the agent identity and persona. <br>
Mitigation: Back up IDENTITY.md and SOUL.md, and install only when persistent adoption of the Haocun/Clawra persona is intended. <br>
Risk: External messaging behavior is under-scoped. <br>
Mitigation: Use least-privilege OpenClaw gateway tokens and require explicit confirmation of channel, recipient, caption, and image before sending. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qidu/get-up) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [Hosted reference image source](https://cdn.jsdelivr.net/gh/christoagent/haoclaw@main/assets/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown instructions, bash commands, and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OpenClaw CLI or a local gateway API to send selected hosted image URLs to configured channels.] <br>

## Skill Version(s): <br>
1.0.5 (source: evidence release, package.json, manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
