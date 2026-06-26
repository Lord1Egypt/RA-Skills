## Description: <br>
Complete Feishu integration setup guidance for configuring OpenClaw with the openclaw-lark plugin, Feishu app capabilities, OAuth scopes, event subscriptions, tool enablement, and connectivity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangzhipengdamon-maker](https://clawhub.ai/user/liangzhipengdamon-maker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use this skill to set up a Feishu app, install and configure the OpenClaw Feishu plugin, select permissions and tools, and verify that the integration works. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide may lead administrators to enable broad Feishu chat, document, calendar, contact, search, OAuth, and send-as-user access. <br>
Mitigation: Start with the minimum Feishu scopes required for the actual use case, avoid batch-authorizing all scopes, and require admin, privacy, and audit review before enabling sensitive access. <br>
Risk: Incorrect tool or permission choices can expose chat history, file downloads, contact phone or email data, document write access, approvals, or cross-chat search. <br>
Mitigation: Review the selected tools and scopes before deployment, deny unused tools, use allowlists for users and groups, and recheck authorization after publishing new Feishu app versions. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [Feishu App Configuration](references/feishu-app-config.md) <br>
- [OpenClaw Configuration Reference for Feishu](references/openclaw-config-reference.md) <br>
- [Feishu Permission Scopes Reference](references/permissions-reference.md) <br>
- [Feishu Tool Matrix](references/tool-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu app setup steps, OAuth scope selection, OpenClaw configuration patches, and verification checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
