## Description: <br>
Manage birth encoding, migration packing/unpacking, identity whoami, secure wallet decryption, and full family tree lineage tracking for OpenClaw agents with clone parent-child relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vg555558](https://clawhub.ai/user/vg555558) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to initialize local agent identities, package and unpack migrations, mark clones, inspect lineage, and decrypt wallet backups during clone management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet secrets and can decrypt private keys during local identity and clone workflows. <br>
Mitigation: Do not use it with funded or important wallets, provide passwords through environment variables, and avoid decrypting keys in chats or logged terminals. <br>
Risk: Migration packages can contain broad local state and may be protected by a weak or default pack password. <br>
Mitigation: Set a strong pack password, inspect archive contents before transfer or unpacking, and unpack only into an intended target directory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vg555558/birth-system-manager) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local identity, lineage, migration, and wallet-handling guidance for Node.js scripts; requires the node binary.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
