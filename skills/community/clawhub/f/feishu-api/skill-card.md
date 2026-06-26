## Description: <br>
This skill guides agents through direct Feishu Open Platform API usage for OAuth authorization, Bitable batch operations, Drive permissions, and cloud document management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noir-hedgehog](https://clawhub.ai/user/noir-hedgehog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill when plugin tools are insufficient for Feishu workflows, including OAuth user authorization, Bitable batch record changes, Drive permission updates, and file or folder management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make high-impact Feishu changes, including deletes and permission updates. <br>
Mitigation: Use a least-privilege Feishu app, require explicit confirmation before deletes or permission changes, and verify target IDs and affected counts before execution. <br>
Risk: The skill handles sensitive credentials and OAuth tokens. <br>
Mitigation: Read credentials only from an approved credential source, avoid printing secrets or tokens, and request only the minimum required scopes. <br>
Risk: Artifact examples disable TLS certificate verification while handling secrets and tokens. <br>
Mitigation: Replace unverified TLS contexts with normal certificate verification before using real secrets or tokens. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [OAuth 用户授权流程](references/oauth.md) <br>
- [多维表格（Bitable）API](references/bitable.md) <br>
- [云文档（Drive）API](references/drive.md) <br>
- [创建飞书应用](references/app-creation.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/noir-hedgehog/feishu-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python code examples and API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OAuth setup steps, Feishu API payload examples, and batch-operation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
