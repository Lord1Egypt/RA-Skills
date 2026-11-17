## Description:

Search, retrieve, and chat with documents stored in Google Drive folders using semantic vector search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eladrave](https://clawhub.ai/user/eladrave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to index Google Drive folders, retrieve relevant document snippets, answer questions over saved files, and download or store files through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recursively reads Google Drive folder contents, including subfolders and shortcuts.

Mitigation: Use a narrowly scoped folder and review the folder contents before syncing.

Risk: Document text, images, and search queries may be sent to Gemini or OpenAI for OCR and embeddings.

Mitigation: Avoid regulated or highly confidential files unless the deployment has appropriate consent, data handling, and provider controls.

Risk: The local vector index stores raw document text and API keys are kept in a local environment file.

Mitigation: Protect the workspace, restrict file access, rotate exposed keys, and add deletion or cleanup controls for generated indexes.

Risk: Dependencies and command-line tools are installed and executed from the Node and Google Workspace ecosystems.

Mitigation: Pin and review dependencies and run the skill in an isolated environment before broader use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/eladrave/skills/eladrave-filechat-rag)
- [Artifact README](artifact/README.md)
- [OpenAI embeddings API endpoint](https://api.openai.com/v1/embeddings)
- [Gemini embedding API endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and retrieved text snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON vector index files and file attachment instructions when retrieving documents.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
