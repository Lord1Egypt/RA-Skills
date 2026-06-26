## Description: <br>
Helps agents implement a durable file-based memory architecture with core memory files, WAL protocol, typed entries, L1 summaries, compression, recall search, and contradiction detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to scaffold, restructure, or audit persistent memory systems for agents that need continuity across sessions. It is most relevant when the agent has persistent filesystem access and needs durable operating rules, user context, decisions, lessons, and long-term memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable memory files may retain personal identifiers, preferences, decisions, or sensitive workspace context longer than intended. <br>
Mitigation: Store only necessary memory, avoid secrets and unnecessary personal identifiers, and keep generated memory files out of shared contexts. <br>
Risk: Heartbeat-style behavior and optional checks of email, calendar, social, or git sources can over-collect context if integrations are enabled too broadly. <br>
Mitigation: Require explicit opt-in for each external source and keep integrations read-only by default. <br>
Risk: Loading long-term memory in group chats or shared channels could expose private user or agent context. <br>
Mitigation: Treat MEMORY.md and SOUL.md as private files and load them only in appropriate one-to-one sessions. <br>


## Reference(s): <br>
- [Memory File Templates](references/memory-templates.md) <br>
- [Memory Type Taxonomy](references/typing-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/samledger67-dotcom/agent-memory-architecture) <br>
- [Publisher Profile](https://clawhub.ai/user/samledger67-dotcom) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with file templates and structured conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-readable architecture guidance and copy-paste memory file templates; no runtime tool calls or credentials are required by the artifact.] <br>

## Skill Version(s): <br>
98.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
