## Description: <br>
Read and create pastes on copy-paste.cloud, fetch recent public pastes, retrieve a paste by ID, or publish new content via the public API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orti99](https://clawhub.ai/user/orti99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve public or authorized private pastes, view recent public pastes, and publish text or code snippets to copy-paste.cloud from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paste content and the COPYPASTE_API_KEY are sent to copy-paste.cloud during normal use. <br>
Mitigation: Use the skill only with content intended for copy-paste.cloud and a scoped API key from a trusted account. <br>
Risk: Public pastes, and sensitive content placed in private or expiring pastes, may still expose confidential information if used incorrectly. <br>
Mitigation: Do not upload secrets, credentials, private logs, customer data, or proprietary code unless disclosure to copy-paste.cloud is intended; use --private where appropriate and do not rely on expiration or burn-after-read as strong secrecy. <br>


## Reference(s): <br>
- [copy-paste.cloud skill page](https://clawhub.ai/orti99/copypaste) <br>
- [copy-paste.cloud](https://copy-paste.cloud) <br>
- [copy-paste.cloud developer API key page](https://copy-paste.cloud/developer) <br>
- [copy-paste.cloud API base](https://api.copy-paste.cloud) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash command examples and terminal text output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and COPYPASTE_API_KEY for recent-list and create operations; get-by-ID can read public pastes without an API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
