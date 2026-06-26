## Description: <br>
No-code cross-platform automation for ClawHub with WeChat, DingTalk, Feishu, WPS, Tencent Docs, and Aliyun Drive integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operations teams use this skill to define, generate, run, and monitor cross-platform automation workflows for messaging, files, documents, approvals, and audit workflows across supported Chinese productivity platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflows can send messages, upload or share files, create users, and export audit or business data. <br>
Mitigation: Use test accounts first, require preview and approval before execution, and configure destination allowlists before enabling those actions. <br>
Risk: Execution logs and exported reports may expose tokens, business data, or audit data. <br>
Mitigation: Run the skill in an isolated environment and avoid printing, exporting, or sharing sensitive tokens and logs. <br>
Risk: Dependencies are declared with minimum versions, so installs can change over time. <br>
Mitigation: Pin dependencies before using the skill with real accounts or production data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaiyuelv/clawhub-automation) <br>
- [WeChat OAuth endpoint](https://open.weixin.qq.com/connect/oauth2/authorize) <br>
- [WeChat API base](https://api.weixin.qq.com) <br>
- [DingTalk OAuth endpoint](https://oapi.dingtalk.com/connect/oauth2/sns_authorize) <br>
- [DingTalk API base](https://oapi.dingtalk.com) <br>
- [Feishu OAuth endpoint](https://open.feishu.cn/open-apis/authen/v1/index) <br>
- [Feishu API base](https://open.feishu.cn) <br>
- [WPS OAuth endpoint](https://open.wps.cn/oauth2/authorize) <br>
- [Tencent Docs API base](https://docs.qq.com/api) <br>
- [Aliyun Drive API base](https://openapi.aliyundrive.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown, Python snippets, YAML configuration, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or execute workflow definitions that send messages, move or share files, export logs, and manage users when connected to real accounts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/__init__.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
