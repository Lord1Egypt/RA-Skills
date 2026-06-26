## Description: <br>
宝塔面板 PHP 网站管理技能，提供站点创建、删除、启停、PHP 版本切换、域名管理、SSL 证书管理、伪静态管理、数据库管理等功能 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aapanel](https://clawhub.ai/user/aapanel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage BaoTa Panel PHP websites, including site lifecycle operations, domain bindings, PHP versions, SSL certificates, rewrite rules, and databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use administrative BaoTa Panel access to change live websites, files, databases, and SSL settings. <br>
Mitigation: Require explicit user confirmation before site, file, database, or SSL changes and summarize the expected service impact before running commands. <br>
Risk: The skill stores and uses panel credentials and may handle database passwords or SSL private key material. <br>
Mitigation: Treat configuration files and command output as secret, avoid printing full config or database passwords in shared sessions, and restrict use to trusted environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aapanel/btpanel-phpsite) <br>
- [Publisher profile](https://clawhub.ai/user/aapanel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and BaoTa Panel API credentials; commands may affect live sites, databases, files, and SSL settings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
