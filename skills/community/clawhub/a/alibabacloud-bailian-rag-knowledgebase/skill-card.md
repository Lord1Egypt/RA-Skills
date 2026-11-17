## Description:

Provides HTTPS API workflows for listing Alibaba Cloud Bailian knowledge bases, retrieving relevant chunks, and answering questions from those results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and support agents use this skill to query Alibaba Cloud Bailian knowledge bases, select relevant indexes, retrieve document chunks, and compose source-attributed answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal setup can install Alibaba Cloud CLI tooling and create, persist, or delete DashScope API keys.

Mitigation: Review before installing, use an existing least-privileged DASHSCOPE_API_KEY when possible, and grant CreateApiKey/DeleteApiKey only when credential management is intended.

Risk: The skill can write API key material to ~/.aliyun/config.json during automatic key creation.

Mitigation: Run only in environments where writes to the Alibaba Cloud CLI config are acceptable, or configure an existing environment-provided API key before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-bailian-rag-knowledgebase)
- [RAM Policies for Bailian RAG Knowledge Base](references/ram-policies.md)
- [Bailian API Key Console](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/api-key)
- [Bailian Knowledge Base Console](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/knowledge-base)
- [Alibaba Cloud RAM Console](https://ram.console.aliyun.com/users)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON retrieval results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieval output includes knowledge-base index IDs, chunk content, relevance scores, document names, and section titles.]

## Skill Version(s):

0.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
