## Description: <br>
Gives agents persistent, structured long-term memory across sessions, organized by project, client, trade, and domain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to initialize and manage a local memory store so agents can remember, recall, update, search, and archive client, project, trade, and knowledge records across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores client, project, trade, and knowledge history that may contain sensitive business or personal information. <br>
Mitigation: Define what may be stored before use, avoid secrets and payment data, and require confirmation before recording sensitive records. <br>
Risk: Archived records may remain available because the evidence notes no true deletion flow. <br>
Mitigation: Add a real delete or anonymization process for removal requests before using the skill with confidential or regulated data. <br>
Risk: Broad automatic recall can surface stale or inappropriate context in later sessions. <br>
Mitigation: Review recalled memory before acting on it and periodically prune, archive, or correct outdated records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/georges91560/agent-memory-manager) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local workspace files under /workspace/memory and writes audit or error logs for memory operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
