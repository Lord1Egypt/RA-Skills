## Description:

Retrieves concise, multi-document results from a hosted Alibaba Bailian knowledge base for use by AI agents and chatbots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krisyejh](https://clawhub.ai/user/krisyejh)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to let an agent query an approved Alibaba Bailian knowledge base and return vector-retrieved proprietary content for downstream LLM responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve proprietary knowledge-base content and make it available to agent conversations.

Mitigation: Use only knowledge bases whose contents the agent is allowed to disclose, and review access policy before enabling the skill.

Risk: Queries are sent to the hosted Alibaba Bailian/DashScope service using a DashScope API key.

Mitigation: Scope the DASHSCOPE_API_KEY appropriately, store it as a secret, and inform users that their retrieval queries leave the local agent environment.

Risk: The skill depends on KNOWLEDGEBASE_ID to select the backing data source.

Mitigation: Set KNOWLEDGEBASE_ID to the intended knowledge base and verify the configured data source before deployment.

## Reference(s):

- [Bailian Knowledge Base Console](https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base)
- [DashScope Knowledge Base Retrieve Endpoint](https://dashscope.aliyuncs.com/api/v1/indices/pipeline/{knowledgebase_id}/retrieve)
- [ClawHub Skill Page](https://clawhub.ai/krisyejh/skills/bailian-knowledge-retrieve)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON response printed to standard output, with setup and invocation guidance in Markdown shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus DASHSCOPE_API_KEY and KNOWLEDGEBASE_ID environment variables; accepts a query string and optional result count from 1 to 20.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
