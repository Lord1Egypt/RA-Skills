## Description: <br>
Read, write, and manage Feishu documents through the Feishu Open API, including document creation, content reading, formatted appends, image insertion, and OAuth token refresh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windsjj20](https://clawhub.ai/user/windsjj20) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to let an agent create, read, and update Feishu notes in a user's cloud drive after Feishu app setup and OAuth authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Feishu cloud-drive access may allow reads or writes beyond the intended notes workflow. <br>
Mitigation: Use a dedicated Feishu app and account or workspace with only the access needed for the intended documents, and review requested document IDs before execution. <br>
Risk: The documented folder limit is advisory because evidence says it is not enforced. <br>
Mitigation: Do not rely on the folder token as a hard security boundary; validate document locations and permissions outside the skill before use. <br>
Risk: Image insertion can fetch arbitrary image URLs. <br>
Mitigation: Use only trusted image URLs and avoid internal, private, or sensitive network locations. <br>
Risk: OAuth tokens and app credentials are stored locally. <br>
Mitigation: Store credentials with restrictive file permissions, rotate credentials if exposed, and remove local token files when the skill is no longer needed. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Feishu Open API base](https://open.feishu.cn/open-apis) <br>
- [ClawHub skill page](https://clawhub.ai/windsjj20/feishu-notes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text output with Feishu document links, document content, and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu App ID, App Secret, OAuth user token, and optional folder token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
