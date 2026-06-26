## Description: <br>
Agent Swarm Network provides inter-agent messaging, context snapshot and restore, event-driven collaboration, model dispatch notifications, sub-agent management, task routing, file transfer, and network diagnostics for agent coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sarahmirrand001-oss](https://clawhub.ai/user/sarahmirrand001-oss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve context across sessions, coordinate peer agents, route work by agent capability, transfer files, and inspect Pilot Protocol network health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically stores and restores unencrypted session context that may include secrets. <br>
Mitigation: Restrict permissions on ~/.pilot, regularly clear old inbox and received files, and avoid placing credentials or sensitive data in sessions that may be snapshotted. <br>
Risk: The skill depends on an external Pilot Protocol binary and helper scripts for messaging, snapshots, publishing, and daemon control. <br>
Mitigation: Audit and build the Pilot Protocol binary and helper scripts from trusted source before use, and manually gate or disable automatic snapshot and restore behavior where needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sarahmirrand001-oss/agent-swarm-network) <br>
- [Agent Swarm Network homepage](https://agent-swarm-network.vercel.app) <br>
- [Pilot Protocol upstream project](https://github.com/TeoSlayer/pilotprotocol) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON files, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and reads local Pilot Protocol context snapshots, event payloads, file-transfer paths, and diagnostic reports.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter, manifest.json, server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
