## Description: <br>
Discuz! X3.5 企飞版后台管理助手。专门解答 Discuz! 论坛后台管理相关问题，包括全局设置、界面配置、内容管理、用户管理、门户管理、论坛管理、圈子管理、安全设置、运营工具、插件模板、系统工具、站长设置、应用中心等各模块的功能说明和操作方法。当用户询问 Discuz! 后台管理相关问题时触发此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohui1301](https://clawhub.ai/user/guohui1301) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Discuz site administrators and operators use this skill to get step-by-step backend management guidance for Discuz! X3.5 企飞版, including global settings, users, content, forums, security, operations, plugins, templates, tools, and application center tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can provide guidance for irreversible or high-impact Discuz administration actions, such as deletion, database maintenance, or financially sensitive settings. <br>
Mitigation: Verify steps against the deployed Discuz version and keep current backups before deletion, database, upgrade, or migration operations. <br>
Risk: Administrative troubleshooting may tempt users to share production secrets, credentials, API keys, or other sensitive configuration details in chat. <br>
Mitigation: Do not provide production secrets in prompts; redact sensitive values and use the skill as a reference helper rather than a secret-handling workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guohui1301/discuz-admin-assistant) <br>
- [Global settings reference](artifact/references/global.md) <br>
- [Interface settings reference](artifact/references/interface.md) <br>
- [Content management reference](artifact/references/content.md) <br>
- [User management reference](artifact/references/users.md) <br>
- [Portal management reference](artifact/references/portal.md) <br>
- [Forum management reference](artifact/references/forum.md) <br>
- [Group management reference](artifact/references/group.md) <br>
- [Security settings reference](artifact/references/security.md) <br>
- [Operations tools reference](artifact/references/operations.md) <br>
- [Plugins and templates reference](artifact/references/plugins.md) <br>
- [System tools reference](artifact/references/tools.md) <br>
- [Administrator settings reference](artifact/references/admin.md) <br>
- [Application center reference](artifact/references/apps.md) <br>
- [Other Discuz reference](artifact/references/other.md) <br>
- [Discuz article reference](http://www.discuz.org/article-5-1.html) <br>
- [Discuz forum reference](http://www.discuz.org/forum-8-1.html) <br>
- [Discuz thread reference](http://www.discuz.org/thread-27039-1-1.html) <br>
- [Discuz group reference](http://www.discuz.org/group-1288-1.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown prose with step-by-step administration instructions and backend navigation paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only responses; no API calls, tools, or shell commands are invoked by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
