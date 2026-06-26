## Description: <br>
Agent Communication Hub provides agent-to-agent communication for OpenClaw skills with direct messaging, broadcast delivery, pub/sub events, session tracking, offline queues, and SQLite-backed persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imgolye](https://clawhub.ai/user/imgolye) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill when multiple OpenClaw agents need durable local messaging, pub/sub event fan-out, session awareness, offline queueing, and communication history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message payloads, event payloads, metadata, and session records can be retained in the local SQLite database. <br>
Mitigation: Avoid sending API keys, passwords, confidential business data, or personal data unless the deployment has appropriate deletion, retention, access-control, and backup handling. <br>


## Reference(s): <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with TypeScript API examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SQLite-backed message, event, session, subscription, and acknowledgement records through TypeScript APIs.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
