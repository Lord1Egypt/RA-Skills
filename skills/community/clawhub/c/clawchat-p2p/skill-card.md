## Description: <br>
Encrypted peer-to-peer messaging for OpenClaw agents across machines with direct connections, multi-identity, and native wake support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexrudloff](https://clawhub.ai/user/alexrudloff) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure encrypted peer-to-peer messaging between agents on different machines or networks, including inbox polling, multi-identity gateway use, and wake-on-message integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A network-reachable P2P daemon may expose agent messaging to unintended peers if access controls are too broad. <br>
Mitigation: Run it only for trusted agents and replace wildcard peer ACLs with explicit trusted principals before use. <br>
Risk: Remote messages can trigger local OpenClaw wake events. <br>
Mitigation: Disable OpenClaw wake unless needed, or scope wake behavior tightly to trusted identities and expected message prefixes. <br>
Risk: Examples include weak secret-handling and persistence patterns that are not production-hardened. <br>
Mitigation: Use password files or a secret manager, avoid command-line mnemonics or passwords, and harden poll/path and nohup examples before copying them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alexrudloff/clawchat-p2p) <br>
- [README](README.md) <br>
- [Quick Start](QUICKSTART.md) <br>
- [Full Command Reference](REFERENCE.md) <br>
- [OpenClaw Integration Recipes](skills/clawchat/RECIPES.md) <br>
- [OpenClaw Integration Guide](skills/clawchat/OPENCLAW-INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents through network setup, identity management, peer messaging, daemon operation, and OpenClaw wake integration.] <br>

## Skill Version(s): <br>
0.0.3 (source: ClawHub release metadata; package.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
