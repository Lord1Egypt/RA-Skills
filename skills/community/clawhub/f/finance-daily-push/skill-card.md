## Description:

自动生成并推送聚焦 A 股科技板块的早报、晚报和周报，包含行情数据、重要消息解读、宏观利率信息和个股推荐。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kldsw](https://clawhub.ai/user/kldsw)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and operators can use this skill to prepare scheduled or on-demand Chinese-language A-share technology-sector market reports. It is intended for informational reporting workflows and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an embedded reusable TuShare API token.

Mitigation: Remove the embedded token, rotate it before use, and configure a user-owned token through TUSHARE_TOKEN.

Risk: The security evidence reports unencrypted quote data used for financial reports.

Mitigation: Prefer TLS-protected or independently verified quote sources before relying on generated report data.

Risk: Generated stock recommendations may be mistaken for investment advice.

Mitigation: Treat recommendations as informational only and retain the report disclaimer in every generated report.

Risk: Cron examples can create recurring finance report tasks.

Mitigation: Track enabled cron jobs and remove them when recurring reports are no longer wanted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kldsw/skills/finance-daily-push)
- [Publisher profile](https://clawhub.ai/user/kldsw)
- [TuShare token setup](https://tushare.pro/user/token)
- [TuShare registration](https://tushare.pro/register)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with optional command output and JSON data from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese-language morning, evening, and weekly finance reports with source/time labels, stock recommendation rationale, risk levels, and investment disclaimers.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
