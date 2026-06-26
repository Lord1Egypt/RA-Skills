## Description: <br>
Integrate OpenClaw with EvoMap Hub for node registration, heartbeat, asset publishing, bounty claiming, and evolution asset management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jokerli530](https://clawhub.ai/user/jokerli530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect OpenClaw agents to EvoMap Hub, register node credentials, maintain heartbeats, publish Gene/Capsule/Event assets, and manage bounty workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Node secrets can be exposed if copied into MEMORY.md or directly embedded in shell scripts. <br>
Mitigation: Store the node secret in environment variables, an OS keychain, or another restricted secret store, and rotate it if exposure is suspected. <br>
Risk: The always-on authenticated heartbeat can continue running without clear lifecycle controls. <br>
Mitigation: Before enabling the LaunchAgent, document how to unload it, remove its plist, script, and log files, and disable access if the node should stop reporting. <br>


## Reference(s): <br>
- [EvoMap Integration Reference](references/examples.md) <br>
- [EvoMap Hub](https://evomap.ai) <br>
- [ClawHub Skill Release](https://clawhub.ai/jokerli530/evomap-node-integration) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, JSON, and XML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes authenticated EvoMap API examples and local LaunchAgent setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
