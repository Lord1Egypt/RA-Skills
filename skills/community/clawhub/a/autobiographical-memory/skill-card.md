## Description: <br>
Structured personal memory system that enables agents to persist, consolidate, and recall episodic and semantic memories across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyucheneureka](https://clawhub.ai/user/xuyucheneureka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain local long-term memory across sessions by recording important events, decisions, preferences, and project context, then consolidating daily notes into curated semantic memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to retain local long-term memory about the user, projects, preferences, and past conversations. <br>
Mitigation: Avoid storing secrets or highly sensitive personal details, and periodically inspect or delete MEMORY.md and memory/*.md entries that should no longer be retained. <br>
Risk: Memory recall can be incomplete or weak when relevant entries are missing or search terms do not match past notes. <br>
Mitigation: State when records do not contain the requested information, try alternate search phrasing, and record corrected information for future recall. <br>


## Reference(s): <br>
- [Consolidation Reference](references/consolidation.md) <br>
- [Recall Patterns Reference](references/recall-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command examples and generated memory reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local memory notes such as MEMORY.md and memory/YYYY-MM-DD.md when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
