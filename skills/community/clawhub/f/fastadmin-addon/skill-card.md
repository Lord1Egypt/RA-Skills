## Description:

FastAdmin插件开发助手。用于创建、开发和打包FastAdmin应用插件。当用户需要创建FastAdmin插件、开发插件功能、配置插件菜单、数据库、打包插件时使用此skill。支持生成插件目录结构、控制器、模型、视图、配置文件、菜单配置、数据库脚本等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohe4966](https://clawhub.ai/user/xiaohe4966)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create, develop, configure, and package FastAdmin application plugins. It provides scaffold commands, directory conventions, PHP controller and configuration examples, database script patterns, menu setup guidance, and packaging notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or copied FastAdmin scaffold files can overwrite existing site files.

Mitigation: Review file paths and changes before applying them to an existing FastAdmin installation, and test the plugin in staging first.

Risk: Example controller defaults exempt all actions from login and authorization checks.

Mitigation: Restrict no-login and no-right exemptions to intentionally public read-only actions before using generated controllers in production.

## Reference(s):

- [FastAdmin plugin development documentation](https://doc.fastadmin.net/developer/55.html)
- [FastAdmin plugin identifier check](https://www.fastadmin.net/developer/idcheck.html)
- [ClawHub skill page](https://clawhub.ai/xiaohe4966/skills/fastadmin-addon)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with PHP, SQL, INI, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scaffold guidance for files that can overwrite parts of a FastAdmin site and should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
