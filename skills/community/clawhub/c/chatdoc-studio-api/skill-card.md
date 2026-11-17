## Description:

ChatDOC Studio API guides agents through PDF parsing, document chat, agent tasks, retrieval, extraction, uploads, and app management with request and response examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chatdoc](https://clawhub.ai/user/chatdoc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to produce ChatDOC Studio API guidance, request examples, and integration patterns for document upload, parsing, chat apps, agent apps, retrieval, extraction, and app management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples include app deletion flows that can permanently remove application data.

Mitigation: Require a dry run, explicit app ID allowlist, backups, and human confirmation before any DELETE request.

Risk: Using the APIs can upload documents to an external document-processing service.

Mitigation: Avoid confidential, regulated, or customer documents unless organizational approval covers ChatDOC Studio handling, retention, and access controls.

Risk: API examples require bearer-token authentication.

Mitigation: Store ChatDOC Studio API keys in approved secret storage and avoid pasting real tokens into shared prompts, logs, or generated examples.

## Reference(s):

- [ChatDOC Studio API skill page](https://clawhub.ai/chatdoc/skills/chatdoc-studio-api)
- [ChatDOC Studio API base URL](https://api.chatdoc.studio/v1)
- [Uploads API](artifact/uploads/uploads_api.md)
- [PDF Parser API](artifact/parsers/pdf_parser.md)
- [Chat App API](artifact/chat/chat_app.md)
- [Agent App API](artifact/agent/agent_app.md)
- [Content Retrieval App API](artifact/retrieval/rag_app.md)
- [Extract App API](artifact/extraction/extract_app.md)
- [Apps API](artifact/apps/apps.md)
- [Document Status](artifact/docs/document_status.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples, JSON payloads, code snippets, cURL commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ChatDOC Studio API key and may include document-processing API calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
