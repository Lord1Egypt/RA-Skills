## Description: <br>
东方财富妙想提供的金融技能集合，涵盖金融数据查询、资讯搜索、智能选股、自选股管理和模拟组合管理，所有技能均需通过MX_APIKEY进行认证。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QQK000](https://clawhub.ai/user/QQK000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill collection to install and configure Eastmoney Miaoxiang finance skills for market data lookup, financial information search, stock screening, watchlist management, and simulated portfolio workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installation flow deletes and replaces local OpenClaw skill directories before installing the Eastmoney skills. <br>
Mitigation: List or back up matching local skill directories before deletion and confirm the target path before running cleanup commands. <br>
Risk: The reviewed artifact downloads remote ZIP packages that are not included in the artifact and are not integrity-verified there. <br>
Mitigation: Inspect the remote ZIP contents first and verify they come from a trusted provider before installing. <br>
Risk: The skill requires an MX_APIKEY for authenticated requests. <br>
Mitigation: Use a dedicated API key when possible and avoid pasting it into logs, shared terminals, or persistent shell files unless explicitly intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/QQK000/eastmoney-skills) <br>
- [Eastmoney Miaoxiang skills page](https://dl.dfcfs.com/m/itc4) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command blocks and API-key setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MX_APIKEY and downloads remote ZIP packages during installation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
