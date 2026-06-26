## Description: <br>
Manages a local ChromaDB-backed enterprise knowledge base for document upload, document management, semantic search, and retrieval-augmented question answering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apanghu](https://clawhub.ai/user/apanghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, support teams, and developers use this skill to upload enterprise documents, maintain a shared local knowledge base, and answer business or policy questions through retrieval before generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document text, chunks, user queries, and reranking inputs may leave the local machine when DashScope or OpenAI is configured. <br>
Mitigation: Use only approved embedding providers for confidential data, protect API keys, and disclose external processing to operators before deployment. <br>
Risk: The skill uses a shared local knowledge-base directory and supports delete operations. <br>
Mitigation: Restrict filesystem permissions on the shared KB directory and require operator confirmation or backups before delete or reset workflows. <br>
Risk: Server security evidence marks the release as suspicious because external processing, shared storage, and destructive deletion behavior are under-disclosed. <br>
Mitigation: Review before installing in sensitive or enterprise environments and document provider, storage, and deletion behavior for users. <br>


## Reference(s): <br>
- [Enterprise Knowledge Base Manager on ClawHub](https://clawhub.ai/apanghu/enterprise-kb-manager) <br>
- [Publisher profile: apanghu](https://clawhub.ai/user/apanghu) <br>
- [DashScope compatible embedding API endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>
- [README.md](artifact/README.md) <br>
- [QUICKSTART.md](artifact/QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text with inline shell commands, JSON configuration examples, and Python usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces document-management responses, retrieval results, and setup guidance; uploaded document text, chunks, queries, and reranking inputs may be processed by configured embedding providers.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
