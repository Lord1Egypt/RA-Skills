## Description: <br>
Bitchat integration skill for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wkyleg](https://clawhub.ai/user/wkyleg) <br>

### License/Terms of Use: <br>
Unlicense <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to connect agents to a local Bitchat BLE mesh through a configured bitchat-node bridge for peer-to-peer text messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default open inbound messaging can allow nearby Bitchat peers to inject messages into OpenClaw sessions. <br>
Mitigation: Set dmPolicy to allowlist or disabled before enabling the channel, and only allow trusted peer IDs. <br>
Risk: A reachable webhook or bridge can allow callers on the network to inject untrusted messages. <br>
Mitigation: Keep the bridge and webhook bound to localhost or a trusted network, and avoid exposing the OpenClaw gateway publicly. <br>
Risk: Mesh-originated messages may contain untrusted instructions or misleading content. <br>
Mitigation: Treat all mesh-originated messages as untrusted and review downstream agent actions before execution. <br>


## Reference(s): <br>
- [ClawHub Bitchat release page](https://clawhub.ai/wkyleg/bitchat) <br>
- [bitchat-node dependency](https://github.com/wkyleg/bitchat-node) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes inbound and outbound text messages through a local Bitchat bridge; media is not supported.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
