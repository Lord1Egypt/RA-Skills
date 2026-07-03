## Description: <br>
Agent Long-Term Memory gives AI agents a local three-tier memory layer for short-term turns, structured user facts, and episodic semantic recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[exp007](https://clawhub.ai/user/exp007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add local, cross-project memory to AI assistants, including structured profile facts, recent turns, and searchable conversation episodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory may create cross-project user profiles in the default data directory. <br>
Mitigation: Use a project-specific data_dir for sensitive work and periodically review or delete stored memories. <br>
Risk: Conversation text may be sent to OpenAI for extraction or embeddings when OPENAI_API_KEY is configured. <br>
Mitigation: Leave OPENAI_API_KEY unset for local regex-only extraction or review data handling before enabling remote extraction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/exp007/agent-long-term-memory) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/exp007) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or query local SQLite and ChromaDB memory stores when integrated by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
