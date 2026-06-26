## Description: <br>
Manage mihomo proxy - install, configure from subscriptions, monitor health, auto-switch nodes. Supports vmess/ss/trojan/vless protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4ier](https://clawhub.ai/user/4ier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and manage a local mihomo proxy, configure it from subscriptions or proxy URLs, monitor health, and switch nodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and start a persistent privileged network proxy service. <br>
Mitigation: Review before installing, grant sudo only when a persistent service is intended, and verify the mihomo release independently. <br>
Risk: The mihomo controller can expose high-impact proxy controls if bound broadly or left without a secret. <br>
Mitigation: Bind the controller to localhost and configure a controller secret before starting the service. <br>
Risk: Subscription URLs and proxy links can contain credentials or tokens. <br>
Mitigation: Avoid pasting subscription URLs into contexts where logs may be retained, and rotate exposed subscription credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/4ier/claw-use-mihomo) <br>
- [mihomo upstream project](https://github.com/MetaCubeX/mihomo) <br>
- [mihomod npm package](https://www.npmjs.com/package/mihomod) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can create or modify local mihomo configuration files and can start, stop, or monitor a local proxy service.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
