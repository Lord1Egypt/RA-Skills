## Description:

Queries Upkuajing customs import/export data by company ID to summarize trade partner structure, HS-code distribution, product distribution, and monthly trade activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade teams, procurement agents, and analysts use this skill to inspect a company's customs trade partners, compare HS-code and product distributions, and understand monthly trade activity from Upkuajing customs data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an Upkuajing API key and may read credentials from ~/.upkuajing/.env.

Mitigation: Use environment variables or owner-only permissions on the env file, and do not ask the agent to display the credential file contents.

Risk: Customs-data lookups and recharge-related actions can affect a paid API balance.

Mitigation: Confirm costs before each paid lookup and review any recharge order before approving payment.

Risk: Error reporting can send request context to the platform.

Mitigation: Submit error reports only after user confirmation and avoid including sensitive request details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-company-partner-stats-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [公司贸易伙伴趋势 API 参考](references/customs-company-partner-stats-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Natural-language guidance with JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; paid customs-data calls and recharge actions require explicit user confirmation.]

## Skill Version(s):

1.0.2 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
