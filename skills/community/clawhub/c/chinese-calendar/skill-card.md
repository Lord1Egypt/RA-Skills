## Description:

获取中国节假日、调休安排和工作日判断信息，并通过 timor.tech API 提供自动更新的日历查询指导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[teweitao](https://clawhub.ai/user/teweitao)

### License/Terms of Use:


## Use Case:

Agents and automation builders use this skill to check whether China calendar dates are workdays, holidays, weekends, or adjusted work/rest days. It also supports annual holiday schedule lookup and reminder workflows that depend on official public holiday arrangements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar date lookups are sent to the third-party timor.tech API.

Mitigation: Use the skill only where outbound third-party API calls are approved, and avoid confidential planning workflows unless that data sharing is acceptable.

Risk: Holiday and adjusted workday answers depend on third-party maintained data.

Mitigation: For high-impact scheduling decisions, verify important dates against an authoritative public holiday source before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teweitao/skills/chinese-calendar)
- [timor.tech holiday info API example](https://timor.tech/api/holiday/info/2026-02-28)
- [timor.tech annual holiday API example](https://timor.tech/api/holiday/year/2026/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Code, Configuration]

**Output Format:** [Markdown with Bash, PowerShell, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for shell examples; API responses are JSON from timor.tech.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
