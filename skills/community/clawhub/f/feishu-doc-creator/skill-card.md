## Description: <br>
Creates Feishu documents such as bitables, docs, spreadsheets, and slides, then names them, transfers ownership, and sends an interactive card link to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq654704712](https://clawhub.ai/user/qq654704712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to create Feishu documents with app credentials, transfer ownership, and send document links to users. It also supports a weekly-report mode that can assign administrators and set enterprise visibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses app-level Feishu credentials and can automatically change document ownership and sharing visibility. <br>
Mitigation: Install only after trusting the publisher and approving the Feishu app permissions; use a least-privileged Feishu app and review who can invoke the skill. <br>
Risk: The wen_admin mode can transfer control, add managers, and make documents visible across the enterprise. <br>
Mitigation: Restrict access to wen_admin mode and confirm the target app and administrator open IDs before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qq654704712/feishu-doc-creator) <br>
- [Feishu Open Platform - Create Bitable](https://open.feishu.cn/document/zh-cn/bitable-v1/app/create) <br>
- [Feishu Open Platform - Create Document](https://open.feishu.cn/document/zh-cn/docx-v1/document/create) <br>
- [Feishu Open Platform - Transfer Document Owner](https://open.feishu.cn/document/zh-cn/drive-v1/permission/transfer_owner) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Documents] <br>
**Output Format:** [JSON object by default, or plain text when requested; successful output includes document URL, name, type, token, and status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates documents in Feishu and may send an interactive card link to the requesting user.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
