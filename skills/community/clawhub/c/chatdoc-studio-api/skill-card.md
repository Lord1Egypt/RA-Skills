## Description: <br>
ChatDOC Studio API usage guide for PDF parsing, document chat, agent tasks, retrieval, uploads, app management, and structured data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chatdoc](https://clawhub.ai/user/chatdoc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to integrate agents and applications with ChatDOC Studio APIs for uploading documents, parsing PDFs, building document Q&A, running agent tasks, retrieving content, and extracting structured data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive documents, prompts, retrieval queries, conversations, and extracted outputs may be sent to a third-party service. <br>
Mitigation: Review data sensitivity, account scope, and organization policy before using the skill with production ChatDOC accounts or sensitive files. <br>
Risk: The artifact includes app deletion examples that can permanently remove ChatDOC applications and associated data. <br>
Mitigation: Require explicit approval, a dry-run list of exact app IDs, backups or recovery planning, and a token with appropriate scope before running deletion workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chatdoc/chatdoc-studio-api) <br>
- [ChatDOC publisher profile](https://clawhub.ai/user/chatdoc) <br>
- [ChatDOC Studio API base URL](https://api.chatdoc.studio/v1) <br>
- [Uploads API documentation](uploads/uploads_api.md) <br>
- [PDF Parser API documentation](parsers/pdf_parser.md) <br>
- [Chat App API documentation](chat/chat_app.md) <br>
- [Agent App API documentation](agent/agent_app.md) <br>
- [RAG App API documentation](retrieval/rag_app.md) <br>
- [Extract App API documentation](extraction/extract_app.md) <br>
- [Apps API documentation](apps/apps.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with API examples in Python, TypeScript, cURL, JSON, and shell environment configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ChatDOC Studio API key and sends uploaded files, prompts, retrieval queries, conversations, and extracted outputs to a third-party service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
