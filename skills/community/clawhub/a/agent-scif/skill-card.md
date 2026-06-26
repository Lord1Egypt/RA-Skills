## Description: <br>
Agent SCIF manages an encrypted local vault with TOTP authentication and clean-room session isolation so an agent can store, retrieve, and manage secrets without reading them in the main session. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[cmill01](https://clawhub.ai/user/cmill01) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can experiment with sealed-memory workflows that keep vault contents out of the main agent context while allowing authorized vault setup, open, add, delete, list, and close operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real secrets through a long-lived sub-agent, local secret/session files, and direct messaging delivery. <br>
Mitigation: Use it only as an experimental vault on a trusted machine, verify the destination chat before opening the vault, and close the vault promptly. <br>
Risk: Local filesystem access can expose the TOTP seed and encrypted vault material. <br>
Mitigation: Do not treat this as a production secrets manager or hardware-backed key store; avoid high-value credentials unless the local file and session risks are accepted. <br>
Risk: Secrets typed in the main chat can enter the main agent context before they reach the clean room. <br>
Mitigation: Avoid entering sensitive values in the main chat and prefer the documented stdin or clean-room input path when adding vault entries. <br>


## Reference(s): <br>
- [Agent SCIF on ClawHub](https://clawhub.ai/cmill01/agent-scif) <br>
- [Publisher profile: cmill01](https://clawhub.ai/user/cmill01) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and operational status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local vault, TOTP, QR, encrypted vault, and temporary session files; clean-room responses are designed to go directly to the user's configured messaging channel.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
