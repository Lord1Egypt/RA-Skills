## Description: <br>
Persistent memory system for AI agents to remember facts, learn from experiences, recall memories, and track entities across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sieyer](https://clawhub.ai/user/Sieyer) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to give agents local, persistent memory for facts, lessons, and entity context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved memories and exported data can contain private, sensitive, or regulated information. <br>
Mitigation: Avoid storing secrets, credentials, regulated data, or third-party personal details without consent; review or delete the local database periodically and treat exports as sensitive private files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sieyer/agent-memory-1-0-0) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Clawdbot](https://github.com/clawdbot/clawdbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code examples; runtime data is stored in a local SQLite database and can be exported as JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores facts, lessons, and entity records locally at the configured database path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
