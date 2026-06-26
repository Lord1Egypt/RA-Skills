## Description: <br>
将 Markdown 文件发布为飞书（Feishu/Lark）在线文档，支持常见 Markdown 富文本、表格渲染、公开分享配置和发布后文档所有权移交。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happyphper](https://clawhub.ai/user/happyphper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to publish selected local Markdown files as Feishu/Lark DocX documents, optionally placing them in a folder, setting sharing permissions, and transferring ownership to a human account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected Markdown files and referenced images may contain sensitive information and are uploaded to Feishu/Lark. <br>
Mitigation: Review files for secrets and confidential content before publishing, and upload only files intended for Feishu/Lark. <br>
Risk: public-read or public-edit sharing can expose published documents outside the organization. <br>
Mitigation: Use tenant-scoped sharing by default and enable public sharing only when internet access is intended and allowed by policy. <br>
Risk: A wrong FEISHU_ADMIN or owner identifier can transfer document ownership to the wrong account. <br>
Mitigation: Verify FEISHU_ADMIN or the --owner value before running ownership transfer. <br>
Risk: Feishu application credentials can grant document and drive access if leaked or over-scoped. <br>
Mitigation: Use a dedicated Feishu app with the narrowest permissions available and rotate FEISHU_APP_SECRET if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/happyphper/feishu-doc-publisher) <br>
- [Feishu Open APIs](https://open.feishu.cn/open-apis) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration guidance] <br>
**Output Format:** [Terminal text with document metadata, status counts, and a Feishu/Lark document URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus FEISHU_APP_ID and FEISHU_APP_SECRET; FEISHU_ADMIN is optional for ownership transfer.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
