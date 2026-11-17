## Description:

按名称、统一社会信用代码等查企业地址、电话、邮箱与网站等联系方式。当用户说：这家公司的联系电话是多少？总部地址在哪？或类似企业联系方式问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up enterprise contact details such as addresses, phone numbers, email addresses, and websites by company name or Chinese business identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names, credit codes, registration numbers, or organization codes submitted through the skill are sent to JisuAPI.

Mitigation: Submit identifiers only when the lookup is necessary and permitted.

Risk: The skill depends on a JISU_API_KEY for third-party API access.

Mitigation: Use a dedicated, low-quota API key, rotate it periodically, and avoid sharing it in prompts or logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/enterprisecontact)
- [JisuAPI Enterprise Contact API](https://www.jisuapi.com/api/enterprisecontact/)
- [JisuAPI](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JISU_API_KEY environment variable; API lookups send submitted company names or business identifiers to JisuAPI.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
