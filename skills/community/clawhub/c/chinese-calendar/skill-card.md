## Description: <br>
Provides Chinese calendar lookup guidance for holidays, adjusted rest days, and workday checks using the timor.tech API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TEweitao](https://clawhub.ai/user/TEweitao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to check whether China-specific dates are workdays or holidays, retrieve annual holiday schedules, and build reminders that account for adjusted work and rest days. <br>

### Deployment Geography for Use: <br>
Global; calendar data is specific to China. <br>

## Known Risks and Mitigations: <br>
Risk: Date queries are sent to the third-party timor.tech API, which may reveal scheduling intent. <br>
Mitigation: Avoid confidential scheduling or sensitive operational planning and only query dates that are appropriate to share with the service. <br>
Risk: Holiday or workday data may be incorrect, delayed, or differ from official announcements. <br>
Mitigation: Verify critical holiday and workday decisions against an official source before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TEweitao/chinese-calendar) <br>
- [timor.tech Holiday Info API Example](https://timor.tech/api/holiday/info/2026-02-28) <br>
- [timor.tech Annual Holiday API Example](https://timor.tech/api/holiday/year/2026/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Bash and PowerShell command examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for shell examples and sends date queries to timor.tech.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
