## Description: <br>
Enable and configure Moltbot/Clawdbot memory search for persistent context, including MEMORY.md, daily logs, and vector search setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure persistent memory search for Moltbot/Clawdbot workspaces, including provider selection, memory file layout, daily logs, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can make notes and past conversations searchable, including sensitive personal or business context if users index it. <br>
Mitigation: Avoid indexing secrets or highly sensitive data, periodically prune MEMORY.md and memory logs, and review what sources are enabled. <br>
Risk: External embedding providers may receive indexed memory content when configured. <br>
Mitigation: Use the local provider for sensitive work, or confirm provider data handling before enabling Voyage or OpenAI embeddings. <br>
Risk: Session transcript indexing can broaden the amount of historical conversation content available for retrieval. <br>
Mitigation: Disable session transcript indexing unless it is needed for the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cs995279497-byte/chen-memory-setup) <br>
- [Publisher profile](https://clawhub.ai/user/cs995279497-byte) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; may guide creation of local memory files and agent configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
