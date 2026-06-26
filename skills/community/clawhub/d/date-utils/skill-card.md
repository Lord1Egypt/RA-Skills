## Description: <br>
Date Utils helps agents get current dates and times, convert timestamps, compute relative dates, format dates, check weekdays, calculate ISO weeks, and compare date ranges using local Python datetime logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a workflow needs reliable current time, date arithmetic, timestamp conversion, date formatting, weekday checks, ISO week information, or date differences without relying on model memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default Asia/Shanghai (UTC+8) timezone can produce misleading results for workflows that require another local timezone or are near date boundaries. <br>
Mitigation: Confirm the required timezone before using outputs for deadlines, payroll, compliance, scheduling, or records near day boundaries. <br>
Risk: Weekday checks treat Monday through Friday as workdays and do not account for holidays or region-specific calendars. <br>
Mitigation: Verify business-calendar requirements separately before relying on workday output for operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidongkl/date-utils) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON command output interpreted by the agent as text or markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the system clock with an Asia/Shanghai (UTC+8) default and Python standard library date/time calculations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
