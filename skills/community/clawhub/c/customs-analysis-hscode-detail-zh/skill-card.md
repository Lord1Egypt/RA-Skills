## Description:

查询指定 HS 编码的中文和英文描述，帮助用户理解该编码代表的产品类别。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Trade practitioners, analysts, import/export workers, and agents use this skill to look up a specific HS code and retrieve its Chinese and English product classification descriptions before customs, tariff, or trade-data analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid Upkuajing API and can initiate recharge flows.

Mitigation: Confirm expected charges before running paid lookup or recharge commands, and use the pricing command or pricing page for current costs.

Risk: The skill stores and reads an Upkuajing API key from ~/.upkuajing/.env.

Mitigation: Keep the API key out of chat, logs, screenshots, and command output; rotate the key if it may have been exposed.

Risk: Error reports may send diagnostic context and request or response data to the platform.

Mitigation: Approve error reporting only after checking that the payload contains no secrets or private business data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-analysis-hscode-detail-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [HS code detail API reference](references/customs-analysis-hscode-detail-api.md)
- [Skill error report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; HS-code lookup calls return hscode, descZh, descEn, fee information, and requestId when successful.]

## Skill Version(s):

1.0.1 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
