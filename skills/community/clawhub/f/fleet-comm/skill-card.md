## Description: <br>
Enables real-time text messaging and broadcasting between multiple OpenClaw nodes across machines for coordinated fleet operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to coordinate multi-machine OpenClaw fleets by sending direct messages, broadcasts, tasks, status checks, and result messages between registered nodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The message bus is exposed without authentication and can leak or allow tampering with agent messages. <br>
Mitigation: Restrict port 18800 to trusted machines, preferably on a private network with firewall rules. <br>
Risk: Fleet messages may contain sensitive task content and received messages are not authenticated. <br>
Mitigation: Do not send secrets, credentials, or sensitive task content through the bus, and treat received messages as untrusted until authentication, authorization, safer CORS, output escaping, and retention controls are added. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dagangtj/fleet-comm) <br>
- [Fleet Communication Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON message payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Node.js HTTP message bus and CLI to exchange fleet messages; message content should be treated as untrusted.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
