## Description: <br>
Scalable memory system for AI agents with short-term, long-term, and episodic memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add persistent memory, conversation context management, knowledge retrieval, and episodic recall to AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally supports persistent local agent memory, which can retain sensitive user, business, or regulated data if used without a retention plan. <br>
Mitigation: Review the .agent_memory storage location before deployment, avoid storing secrets or regulated personal data, and define deletion and retention procedures. <br>


## Reference(s): <br>
- [Short-Term Memory](references/short-term.md) <br>
- [Long-Term Memory](references/long-term.md) <br>
- [Episodic Memory](references/episodic.md) <br>
- [ClawHub Release Page](https://clawhub.ai/evezart/agent-memory-layer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python code examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local memory-layer code patterns and operational guidance for retention and deletion planning.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
