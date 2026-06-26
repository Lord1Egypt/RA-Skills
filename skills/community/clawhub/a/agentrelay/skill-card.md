## Description: <br>
Reliable agent-to-agent communication protocol for transferring large payloads via shared files with pointer references and secret code verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[extraterrest](https://clawhub.ai/user/extraterrest) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use AgentRelay to pass large inter-agent payloads through shared files while sending compact pointer messages and completion confirmations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad automatic triggers may cause agents to process relay messages that were not intentionally authorized. <br>
Mitigation: Use exact structured AgentRelay triggers only with trusted agents and require clear sender authorization before acting on a relay event. <br>
Risk: Insufficiently constrained event IDs or file pointers can create unsafe file access patterns. <br>
Mitigation: Validate event IDs and pointers strictly before receiving, updating, verifying, or cleaning relay files. <br>
Risk: Relay storage, logs, registry entries, and secrets may retain sensitive payload metadata. <br>
Mitigation: Run in a low-privilege environment, document retention and privacy handling, and use receiver-controlled deletion or cleanup for expired events. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/extraterrest/agentrelay) <br>
- [ClawHub manifest](artifact/clawhub.json) <br>
- [README](artifact/README.md) <br>
- [Release notes](artifact/RELEASE_NOTES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compact AgentRelay CSV pointer messages and JSON command output when its helper scripts are run.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
