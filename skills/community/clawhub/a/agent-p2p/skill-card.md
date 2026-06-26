## Description: <br>
Agent P2P enables AI agents to communicate in real time through user-managed Portals, using send.py for message exchange and contact management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yananli199307-dev](https://clawhub.ai/user/yananli199307-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to deploy and operate Portal-based P2P messaging, file transfer, owner chat, and contact approval workflows between AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local and VPS control, including SSH deployment, systemd services, and command execution, can affect host integrity. <br>
Mitigation: Use a dedicated VPS and dedicated SSH key, review commands before execution, and restrict access to only the Portal host. <br>
Risk: The skill handles API keys, hooks tokens, admin credentials, shared keys, and SSH material. <br>
Mitigation: Store credentials in the documented environment files only, rotate hooks/API/admin credentials after testing, and avoid sharing OWNER_KEY values. <br>
Risk: The security summary flags unsafe handling of public endpoints, plaintext secrets, endpoint authentication, file-transfer approval, and command injection concerns. <br>
Mitigation: Inspect the deploy source before installation and avoid sensitive file transfers until those issues are fixed. <br>
Risk: Direct file transfer can upload files to a receiving Portal without a separate receiver approval step. <br>
Mitigation: Confirm contacts and destination Portal URLs before transfer, and use the skill only with trusted counterparties. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yananli199307-dev/agent-p2p) <br>
- [README](README.md) <br>
- [Configuration Guide](CONFIG.md) <br>
- [Environment Variables](ENV.md) <br>
- [Deployment Guide](DEPLOY.md) <br>
- [Verification Refactor Design](docs/verification-refactor.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local commands, VPS deployment steps, environment variable edits, and message or file transfer commands.] <br>

## Skill Version(s): <br>
0.9.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
