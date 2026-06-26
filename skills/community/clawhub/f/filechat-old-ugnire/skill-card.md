## Description: <br>
Searches, retrieves, and answers questions over documents in a designated Google Drive folder using semantic vector search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eladrave](https://clawhub.ai/user/eladrave) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to sync a selected Google Drive folder, search indexed document chunks, answer questions with cited file names, and retrieve matching files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recursively copy private Google Drive files and persist searchable local indexes. <br>
Mitigation: Use a dedicated low-risk Drive folder, avoid regulated or highly confidential documents, and confirm how to delete local indexes and downloaded files. <br>
Risk: Document text, images, and search queries may be sent to Gemini for OCR or embeddings. <br>
Mitigation: Restrict API keys, sync only documents approved for Gemini processing, and review consent and data-handling requirements before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eladrave/filechat-old-ugnire) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets and plain-text query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Query results include matching file names, Google Drive file IDs, similarity scores, and snippets when the local index exists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
