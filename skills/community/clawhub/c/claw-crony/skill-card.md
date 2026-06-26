## Description: <br>
Installs and configures the Claw Crony A2A Gateway plugin for cross-server OpenClaw agent communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccccl8](https://clawhub.ai/user/ccccl8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators setting up two or more OpenClaw servers use this skill to install the gateway plugin, configure peer discovery, bearer authentication, routing, and verification for A2A messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exposing an A2A gateway can allow trusted peers to initiate persistent remote-agent requests. <br>
Mitigation: Review and pin the external plugin code, prefer Tailscale or a private LAN, firewall port 18800 to known peer IPs, and avoid public HTTP exposure. <br>
Risk: Bearer tokens used for peer access can be copied or exposed if placed in agent-facing setup material. <br>
Mitigation: Do not put raw bearer tokens in TOOLS.md, share tokens only with trusted peers, and rotate any token that may have been exposed. <br>
Risk: Forwarding prompts to another agent can disclose user content or trigger unintended remote work. <br>
Mitigation: Require clear user intent before forwarding messages to another agent and verify the selected peer before sending. <br>


## Reference(s): <br>
- [Claw Crony on ClawHub](https://clawhub.ai/ccccl8/claw-crony) <br>
- [TOOLS.md A2A Section Template](references/tools-md-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes placeholders for local paths, peer URLs, bearer tokens, and agent identifiers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
