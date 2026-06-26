## Description: <br>
Context Continuity helps an agent resume prior work by reading local memory files and automatically writing concise daily conversation summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CJstate](https://clawhub.ai/user/CJstate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preserve and resume project context across conversations by summarizing recent tasks, decisions, progress, and todos from local memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic local conversation-memory storage can preserve sensitive or private information with limited user control. <br>
Mitigation: Install only where local memory storage is acceptable, avoid using it around secrets or private data, and review or delete memory files regularly. <br>
Risk: Automatically loading prior memory can reintroduce stale or unintended context into a new conversation. <br>
Mitigation: Review the generated context summary before acting and adjust or remove outdated memory entries when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CJstate/context-continuity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces concise context summaries and local memory file updates when followed by the agent.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
