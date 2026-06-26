## Description: <br>
Persistent memory system for AI agents - remember facts, learn from experience, and track entities across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local persistent memory to AI-agent workflows, including fact recall, lessons learned, and entity context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local memory database can contain sensitive cross-session facts or personal data. <br>
Mitigation: Treat the database as sensitive, avoid storing secrets or private personal data without consent, and use expirations or cleanup for stale facts. <br>
Risk: Recalled memory may be stale, incomplete, or poisoned and could influence important actions. <br>
Mitigation: Review recalled memory before letting an agent take consequential actions such as deploying, sending messages, modifying access, or deleting data. <br>
Risk: Entity tracking can become covert profiling when people are stored without a clear task reason or user awareness. <br>
Mitigation: Track people only for clear current tasks with user awareness, and keep entity context transparent. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/agent-memory-hardened) <br>
- [README](README.md) <br>
- [Safety evaluation](SAFETY.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Clawdbot](https://github.com/clawdbot/clawdbot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; memory operations produce text records and JSON exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite memory database by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
