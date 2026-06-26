## Description: <br>
Feishu Log structures user-provided meeting notes, project updates, work reviews, and event logs, then writes them to Feishu documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonyvics](https://clawhub.ai/user/tonyvics) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to turn provided work notes into structured Feishu documents for meetings, project logs, work reviews, important events, and learning notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded Feishu credentials or tokens may expose an app or tenant if reused. <br>
Mitigation: Remove embedded credentials before installation, rotate any exposed secrets, and configure a tenant-owned Feishu app. <br>
Risk: Broad tenant-level Feishu permissions can create or edit cloud documents and manage drive resources beyond the intended log. <br>
Mitigation: Use a least-privilege Feishu app and confirm the requested Drive, Docx, folder, and permission scopes before use. <br>
Risk: Plaintext local secret storage can leak App Secrets on shared or poorly protected machines. <br>
Mitigation: Prefer a managed secret store when available and restrict access to any ~/.openclaw credential files. <br>
Risk: Automatic full-access collaborator sharing can expose sensitive meeting notes or work records to the wrong account. <br>
Mitigation: Verify the destination folder, collaborator open_id, and permission level before writing sensitive logs. <br>


## Reference(s): <br>
- [ClawHub Feishu Log release](https://clawhub.ai/tonyvics/feishu-log) <br>
- [Feishu Open Platform documentation](https://open.feishu.cn/document) <br>
- [Feishu Drive API documentation](https://open.feishu.cn/document/ukTMukTMukTM/ucDM54SOy4DNL4SM2gTN) <br>
- [Feishu Docx API documentation](https://open.feishu.cn/document/ukTMukTMukTM/uYjNwUjL2YDM14iN2gTN) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Structured Markdown guidance, shell command examples, configuration values, and Feishu API calls that create folders, documents, and permissions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, curl, jq, Feishu app credentials, and a collaborator open_id; writes content to Feishu cloud documents.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
