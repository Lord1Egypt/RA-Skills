## Description:

查询北京住宅小区的基础信息（房价/区域/交通），并通过官方验证渠道核实学区划片信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamhankai](https://clawhub.ai/user/iamhankai)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to look up Beijing residential community prices, districts, transit clues, and school zoning verification paths. It is scoped to Beijing and emphasizes official or manually verified school assignment sources.

### Deployment Geography for Use:

China (Beijing)

## Known Risks and Mitigations:

Risk: The skill may submit a community name or precise address to external housing and education websites.

Mitigation: Ask for user consent before lookup, avoid precise home addresses when possible, and prefer manual browser verification for sensitive queries.

Risk: The school lookup launches a browser with no-sandbox against an HTTP education site.

Mitigation: Run only in an isolated virtual environment or container under a low-privilege account, and remove no-sandbox before broader deployment.

Risk: Housing prices and school zoning can become outdated or vary by annual policy updates.

Mitigation: Show source and date context, and require confirmation against the current education authority notice before relying on school assignment results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iamhankai/skills/beijing-house-pro)
- [Beike Beijing community search](https://bj.ke.com/xiaoqu/rs{community_name}/)
- [Chaoyang official school lookup](http://xqcx.bjchyedu.cn/)
- [Beijing compulsory education enrollment service platform](http://yjrx.bjedu.cn/)
- [Haidian district education portal](https://www.bjhd.gov.cn/kjhd/)
- [Haidian 2025 school district source data](http://bj.bendibao.com/edu/2022425/313157.shtm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON-formatted script results and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include official lookup URLs, manual verification steps, and time-sensitivity notices for school zoning results.]

## Skill Version(s):

1.0.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
