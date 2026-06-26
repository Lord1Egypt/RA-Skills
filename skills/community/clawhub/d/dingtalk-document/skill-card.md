## Description: <br>
Provides workflows and command guidance for managing DingTalk knowledge bases and documents, including listing workspaces, reading and writing document content, creating or deleting documents, and managing members. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breath57](https://clawhub.ai/user/breath57) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent prepare and run DingTalk document-management workflows such as workspace discovery, document creation, content updates, deletion, and member-permission changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite, delete, or change access to DingTalk business documents. <br>
Mitigation: Require manual confirmation before destructive writes, deletes, or member-permission changes, and use a least-privilege DingTalk app. <br>
Risk: The helper stores DingTalk app credentials and cached tokens in a local config file. <br>
Mitigation: Restrict access to ~/.dingtalk-skills/config, avoid printing secrets, and rotate credentials if the file is exposed. <br>
Risk: Cached tokens may be invalidated before the helper's expiry time. <br>
Mitigation: On DingTalk 401 responses, refresh the token without using the cache before retrying. <br>


## Reference(s): <br>
- [DingTalk API reference bundled with skill](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/breath57/dingtalk-document) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to create temporary shell scripts for multi-step DingTalk API calls; generated operations depend on user-provided DingTalk credentials and document identifiers.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
