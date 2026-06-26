## Description: <br>
通用飞书文档搜索助手，根据配置的文档根目录和触发条件，在指定 Feishu 文档空间及其子目录中搜索信息并回答用户问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carolyn0719](https://clawhub.ai/user/carolyn0719) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to configure a Feishu document or wiki space, search recursively across supported document types, and answer knowledge questions with source links. It can also route configured technical questions to a designated collaborator when that forwarding is approved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports exposed Feishu credentials. <br>
Mitigation: Remove the secret, rotate the Feishu application credentials, and verify that no deployed configuration still uses the exposed values before installation. <br>
Risk: The release evidence reports that some questions may be sent outside the configured document space. <br>
Mitigation: Narrow forwarding triggers and require explicit user approval before sending content to another bot or person. <br>
Risk: The configured workspace and owner override may not match the installer environment. <br>
Mitigation: Confirm the Feishu workspace, root document space, owner settings, and access scope before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/carolyn0719/feishu-doc-searcher) <br>
- [Feishu Open Platform Documentation](https://open.feishu.cn/document/) <br>
- [Feishu Docs API Overview](https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/docs-overview) <br>
- [Feishu Wiki API Overview](https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/wiki-overview) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown answers with cited source links and optional Feishu API command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches configured Feishu spaces recursively and supports docx, sheet, bitable, and board content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
