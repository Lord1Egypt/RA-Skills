## Description: <br>
Search, retrieve, and chat with documents stored in Google Drive folders using semantic vector search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eladrave](https://clawhub.ai/user/eladrave) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to index selected Google Drive folders, retrieve matching document snippets, answer questions over saved files, and download previously stored documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private Google Drive content, credentials, and user search queries. <br>
Mitigation: Install only after reviewing Drive access scope, configuring secrets outside committed files, and confirming that selected document contents may be processed by Gemini or OpenAI. <br>
Risk: Document contents and embeddings may be stored in local JSON files or Qdrant. <br>
Mitigation: Avoid syncing highly sensitive folders until retention, deletion, and opt-in controls are clear for the deployment environment. <br>
Risk: The security review flags under-disclosed and unsafe patterns, including a native-OCR misstatement, embedded credentials, and folder ID validation concerns. <br>
Mitigation: Review the publisher's security guidance before deployment and verify OCR behavior, credential handling, and folder identifiers during setup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eladrave/filechat-rag) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and retrieved text snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Google Drive file IDs, vector-search matches, local JSON backups, or Qdrant search results.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
