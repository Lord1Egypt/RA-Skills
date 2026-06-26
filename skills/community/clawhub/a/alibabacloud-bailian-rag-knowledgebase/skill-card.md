## Description: <br>
Alibaba Cloud Bailian Knowledge Base Retrieval Tool. Use HTTPS API to query and retrieve knowledge base content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to list Alibaba Cloud Bailian knowledge bases, retrieve relevant chunks from selected indices, and answer user questions with source document and section context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an Alibaba Cloud CLI profile and can create, store, or delete DashScope API keys. <br>
Mitigation: Prefer providing DASHSCOPE_API_KEY directly; grant CreateApiKey and DeleteApiKey permissions only when automatic key provisioning and revocation are intended, and review ~/.aliyun/config.json after use. <br>
Risk: The skill may install the Alibaba Cloud ModelStudio CLI plugin using a pre-release plugin flag. <br>
Mitigation: Review the CLI plugin installation step and run it only in an environment where that Alibaba Cloud CLI profile is intended for this workflow. <br>
Risk: The skill requires sensitive credentials for Bailian knowledge base retrieval. <br>
Mitigation: Use least-privilege RAM permissions and avoid exposing DashScope API keys in generated files, logs, terminal output, or agent responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-bailian-rag-knowledgebase) <br>
- [RAM Policies for Bailian RAG Knowledge Base](references/ram-policies.md) <br>
- [Bailian API Key Console](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/api-key) <br>
- [Bailian Knowledge Base Console](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/knowledge-base) <br>
- [Alibaba Cloud RAM Console](https://ram.console.aliyun.com/users) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Retrieval results include knowledge base IDs, chunk content, relevance scores, document names, and section titles.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
