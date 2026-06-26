## Description: <br>
Bailian KnowledgeBase Retrieve queries a configured Alibaba Bailian/DashScope hosted knowledge base and returns concise multi-document retrieval results for LLM-powered agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krisyejh](https://clawhub.ai/user/krisyejh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to let an agent retrieve relevant documents from a configured Bailian/DashScope knowledge base containing proprietary vectorized data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Retrieved knowledge-base text may contain untrusted content that conflicts with agent instructions. <br>
Mitigation: Treat retrieved text as context only, and keep system and developer instructions authoritative. <br>
Risk: Overbroad API credentials or connected knowledge bases may expose data the agent should not access. <br>
Mitigation: Use a narrowly scoped DASHSCOPE_API_KEY and connect only approved knowledge bases that do not contain secrets the agent should not see. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/krisyejh/bailian-knowledge-retrieve) <br>
- [Bailian KnowledgeBase console](https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON retrieval response from the command-line helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, DASHSCOPE_API_KEY, KNOWLEDGEBASE_ID, and network access to DashScope; result count defaults to 5 and is limited to 1-20.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
