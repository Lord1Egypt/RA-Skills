## Description: <br>
Persistent memory system enabling AI agents to remember facts, learn from experiences, and track entities across sessions for improved context awareness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Liguang00806](https://clawhub.ai/user/Liguang00806) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add local SQLite-backed memory for facts, lessons, and entity context across agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed release has inconsistent package identity and install instructions. <br>
Mitigation: Confirm that users intend to install agent-memory-temp or agent-memory and verify the publisher/source before installation. <br>
Risk: The local SQLite memory database can contain sensitive user, project, or relationship data. <br>
Mitigation: Avoid storing secrets or regulated personal data, set retention expectations, and periodically review, export, or delete stored memories. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Liguang00806/agent-memory-temp) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists facts, lessons, and entity records in a local SQLite database by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
