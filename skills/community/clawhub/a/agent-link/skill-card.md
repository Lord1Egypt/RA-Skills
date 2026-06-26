## Description: <br>
Enables OpenClaw agents to communicate peer-to-peer using AgentLink for messaging, contact management, status checks, and identity sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dolutech](https://clawhub.ai/user/dolutech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let OpenClaw agents connect to AgentLink nodes, exchange messages, manage contacts, share agent cards, and inspect node status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote-agent trust flows can expose broad file, calendar, and web actions. <br>
Mitigation: Require explicit approval and allowlists before enabling file, calendar, or web-related intents. <br>
Risk: Trusted contacts may auto-accept sensitive actions if configured too broadly. <br>
Mitigation: Keep new contacts at ask or unknown and avoid trusted auto-accept settings unless the remote agent has been verified. <br>
Risk: The integration depends on an external AgentLink package and node runtime. <br>
Mitigation: Review the external package before installation and install only when an AgentLink P2P node is intentionally required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dolutech/agent-link) <br>
- [AgentLink protocol repository](https://github.com/dolutech/agent-link) <br>
- [AgentLink npm package](https://www.npmjs.com/package/@dolutech/agent-link) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline commands, configuration snippets, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are instructions and command patterns for an agent; networked AgentLink behavior depends on the external package and node configuration.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
