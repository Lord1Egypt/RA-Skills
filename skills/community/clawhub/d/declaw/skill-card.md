## Description: <br>
Direct encrypted peer-to-peer messaging between OpenClaw agents over Yggdrasil IPv6 with peer discovery and connectivity diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jing-yilin](https://clawhub.ai/user/Jing-yilin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Declaw to discover peers, exchange signed direct messages, and diagnose Yggdrasil IPv6 connectivity between agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation and networking instructions may grant broad system and network authority. <br>
Mitigation: Review the Yggdrasil setup path before use, prefer verified package-manager or pinned release installs, and verify binaries before placing them in PATH. <br>
Risk: Piping remote installation scripts into sudo can execute unreviewed code with elevated privileges. <br>
Mitigation: Inspect and pin setup scripts or use package-manager installation where practical instead of running remote scripts directly with sudo. <br>
Risk: Participation in a discoverable peer-to-peer network can expose agent availability and message endpoints to untrusted peers. <br>
Mitigation: Do not send sensitive content to bootstrap AI agents or untrusted peers; verify peer addresses and use the documented TOFU flow before messaging new peers. <br>


## Reference(s): <br>
- [Declaw ClawHub page](https://clawhub.ai/Jing-yilin/declaw) <br>
- [Peer Discovery](references/discovery.md) <br>
- [IPv6 P2P Example Interaction Flows](references/flows.md) <br>
- [Yggdrasil Installation Guide](references/install.md) <br>
- [Bootstrap node list](https://resciencelab.github.io/DeClaw/bootstrap.json) <br>
- [Yggdrasil releases](https://github.com/yggdrasil-network/yggdrasil-go/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with tool-call names, JSON configuration examples, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include peer IPv6 addresses, message text, aliases, ports, and Yggdrasil setup commands.] <br>

## Skill Version(s): <br>
0.3.2 (source: artifact SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
