## Description: <br>
Persistent memory system for AI agents to remember facts, learn from experience, track entities, and recall context across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cxz9909](https://clawhub.ai/user/cxz9909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add local persistent memory to AI agents, including durable facts, lessons learned, entity records, and recall across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist personal facts and conversation-derived context on disk across sessions. <br>
Mitigation: Avoid storing secrets, regulated data, or highly sensitive personal details unless there is consent and a deletion process. <br>
Risk: The local memory database can retain stale or unnecessary information beyond the session where it was collected. <br>
Mitigation: Review the configured database path and periodically purge stale or unnecessary memories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cxz9909/cxz9909-agent-memory) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Clawdbot](https://github.com/clawdbot/clawdbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks, plus local SQLite-backed memory records when used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores facts, lessons, and entity context in a configurable local SQLite database; no external Python dependencies are declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
