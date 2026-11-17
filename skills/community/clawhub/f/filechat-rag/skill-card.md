## Description:

Search, retrieve, and chat with documents stored in Google Drive folders using semantic vector search, incremental sync, OCR, and local JSON or Qdrant-backed vector storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eladrave](https://clawhub.ai/user/eladrave)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use Filechat to sync Google Drive folders into a searchable document library, retrieve relevant snippets, answer questions over saved files, and download or upload files through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recursively read Google Drive folders and persist raw document chunks locally or in Qdrant.

Mitigation: Use only non-sensitive folders until data retention controls are documented, restrict folder access, and review stored vector and metadata files after sync.

Risk: Document contents may be sent to embedding or OCR providers during sync and query workflows.

Mitigation: Confirm provider configuration before use and avoid processing confidential folders unless the selected provider and account meet the user's data handling requirements.

Risk: The artifact includes test credentials and security guidance calls for credential removal or rotation.

Mitigation: Remove bundled credentials from installed copies and rotate any exposed Google Workspace or Gemini credentials before deployment.

Risk: The security guidance identifies safer subprocess calls, folder ID validation, and explicit deletion confirmation as missing controls.

Mitigation: Review command construction and folder inputs before execution, and require explicit user confirmation before deleting cache or vector database files.

## Reference(s):

- [Filechat ClawHub Skill Page](https://clawhub.ai/eladrave/skills/filechat-rag)
- [eladrave Publisher Profile](https://clawhub.ai/user/eladrave)
- [Google Workspace CLI package](https://www.npmjs.com/package/@googleworkspace/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and text snippets from retrieved documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local vector database files, metadata cache files, Google Drive uploads or downloads, and Qdrant collection updates when configured.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
