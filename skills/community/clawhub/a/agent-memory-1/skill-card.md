## Description: <br>
Persistent memory system for AI agents to remember facts, learn from experience, and track entities across sessions with easy recall and updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tigertamvip](https://clawhub.ai/user/tigertamvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local persistent memory so agents can store facts, lessons, and entity context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists agent memory locally, and stored facts, lessons, or entity attributes may contain sensitive information. <br>
Mitigation: Treat the SQLite database as sensitive, avoid storing secrets or regulated personal data, and periodically review, export, or delete stored memories. <br>
Risk: Persistent memory can keep outdated or incorrect context across sessions. <br>
Mitigation: Use expiration, cleanup, superseding, and deletion workflows to remove stale or inaccurate memories. <br>


## Reference(s): <br>
- [Agent Memory 1 on ClawHub](https://clawhub.ai/tigertamvip/agent-memory-1) <br>
- [Publisher profile](https://clawhub.ai/user/tigertamvip) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local SQLite storage by default and supports custom database paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
