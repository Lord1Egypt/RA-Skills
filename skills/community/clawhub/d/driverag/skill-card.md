## Description: <br>
Use the Google Drive RAG CLI to search your synced personal documents, add tracking folders, or check the service account status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eladrave](https://clawhub.ai/user/eladrave) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to query a Google Drive RAG API for answers from synced personal documents, inspect indexed files, check sync status, add folders, trigger syncs, and renew access tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private Google Drive document data through a remote RAG API. <br>
Mitigation: Install only when the Drive RAG API operator is trusted, and avoid sharing returned answers, citations, or file listings beyond the intended user. <br>
Risk: The skill stores and renews bearer tokens and may expose renewed tokens in terminal output. <br>
Mitigation: Use a limited, short-lived token, protect the plaintext .env file, avoid sharing terminal output from token renewal, and require explicit confirmation before renewing tokens. <br>
Risk: The skill can add folders, sync documents, and force complete re-indexing of Drive data. <br>
Mitigation: Require explicit confirmation before adding folders, syncing, or using force re-indexing, and verify the target folders before running those commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eladrave/driverag) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI output may include RAG answers, citations, indexed file lists, sync status, service account details, and token renewal results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
