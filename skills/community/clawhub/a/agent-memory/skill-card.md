## Description: <br>
Persistent memory for AI agents to store facts, learn from actions, recall information, and track entities across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dennis-Da-Menace](https://clawhub.ai/user/Dennis-Da-Menace) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to give AI agents local cross-session memory for durable facts, lessons, entity context, and recall during future work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive or unnecessary personal information in a local SQLite database. <br>
Mitigation: Do not store API keys, passwords, financial details, confidential business data, or unnecessary personal information; periodically review or delete the database. <br>
Risk: Cross-session memory may mix context across projects or users when the default database path is shared. <br>
Mitigation: Use a separate custom database path for different projects or users. <br>


## Reference(s): <br>
- [Agent Memory ClawHub Release](https://clawhub.ai/Dennis-Da-Menace/agent-memory) <br>
- [Publisher Profile](https://clawhub.ai/user/Dennis-Da-Menace) <br>
- [README](README.md) <br>
- [Skill Instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Python API calls, shell commands, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and retrieves local SQLite-backed memory records; default database path is ~/.agent-memory/memory.db.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
