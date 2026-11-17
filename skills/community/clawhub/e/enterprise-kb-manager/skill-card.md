## Description:

Enterprise Knowledge Base Manager helps agents upload, manage, search, and answer questions from enterprise documents using a local ChromaDB-backed knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apanghu](https://clawhub.ai/user/apanghu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, support teams, and developers use this skill to build and operate an enterprise knowledge base for document upload, semantic retrieval, and RAG-style question answering over PDF, DOCX, TXT, and Markdown content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded document text, search queries, and reranked passages may be transmitted to configured external embedding or compatible API providers.

Mitigation: Review provider configuration before use, lock allowed endpoints, protect API keys, and avoid uploading confidential documents unless external transmission is approved.

Risk: Shared knowledge-base storage and delete or reset commands can affect data used by multiple agents.

Mitigation: Run the skill under a restricted account, use external access controls, and keep backups before enabling document deletion or reset workflows.

Risk: Documented privacy and access-control claims may overstate the protections provided by the artifact.

Mitigation: Validate the deployment with independent controls and do not rely on the skill alone for tenant isolation, confidentiality, or policy enforcement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apanghu/skills/enterprise-kb-manager)
- [Publisher profile](https://clawhub.ai/user/apanghu)
- [DashScope compatible API endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create and update local knowledge-base files, vector database entries, document chunks, and retrieval responses.]

## Skill Version(s):

1.1.0 (source: server release evidence and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
