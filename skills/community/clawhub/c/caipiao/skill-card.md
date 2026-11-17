## Description:

查彩票分类、最新与历史开奖、号码是否中奖等。当用户说：双色球最新开奖号码？大乐透上期结果？或类似彩票开奖问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer lottery drawing questions, including lottery categories, latest or historical draw results, and whether submitted numbers won.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lottery lookup inputs, including submitted numbers for winning checks, are sent to JisuAPI.

Mitigation: Use the skill only for inputs the user is comfortable sharing with JisuAPI.

Risk: The JisuAPI app key is used in API requests and could be exposed through verbose HTTP logging or copied command output.

Mitigation: Use a dedicated JisuAPI key with quota or billing limits, avoid logging full request URLs, and rotate the key if it is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/caipiao)
- [JisuAPI lottery drawing API](https://www.jisuapi.com/api/caipiao/)
- [JisuAPI homepage](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the requests Python package, and JISU_API_KEY for live API calls.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
