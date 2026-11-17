## Description:

Search, retrieve, and chat with documents stored in a designated Google Drive folder using semantic retrieval, local indexing, Gemini embeddings, and OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eladrave](https://clawhub.ai/user/eladrave)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to sync a selected Google Drive folder into a local searchable index, answer questions over saved documents, retrieve matching files, and add new documents to the library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drive document contents and user queries may be sent to Google Gemini for embeddings and image OCR.

Mitigation: Only point the skill at Drive folders whose contents are acceptable for that data flow, and avoid highly sensitive folders unless the user accepts it.

Risk: Indexed document text is stored locally in plaintext in vector_db.json with weak containment.

Mitigation: Protect the workspace, .env file, and vector_db.json, and document how to delete or flush the local index.

Risk: The skill broadly copies and indexes files from the configured Drive folder and subfolders.

Mitigation: Use a scoped Drive folder, review sync behavior before installation, and prefer versions with explicit confirmation and scoped sync controls.

Risk: The security verdict is suspicious because the skill handles sensitive files and uses command execution and unpinned dependency ranges.

Mitigation: Review and scan the skill before deployment, pin dependencies, and prefer safer command execution patterns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eladrave/skills/filechat-old-ugnire)
- [Publisher profile](https://clawhub.ai/user/eladrave)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, retrieved text snippets, file identifiers, and optional media attachment references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, gws, GEMINI_API_KEY, and FILECHAT_DRIVE_FOLDER_ID; sync creates a local vector_db.json index from Drive content.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
