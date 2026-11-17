## Description:

Query employee data, time clock entries, schedules, and requests. Requires authentication - employees see own data, managers see team.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianppetty](https://clawhub.ai/user/brianppetty)

### License/Terms of Use:


## Use Case:

Farm employees, managers, and admins use this skill to retrieve workforce information, manage time clock and schedule workflows, capture availability or time-off requests, and route approvals with role-scoped access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive employee data, including payroll exports, roles, activity status, and GPS-related time clock fields.

Mitigation: Use only in a controlled FarmOS environment with authenticated employee-directory access, role enforcement, and private or HTTPS-equivalent transport.

Risk: The skill can initiate state-changing workforce actions such as clock events, request submission, approvals, rejections, exports, and shared schedule notifications.

Mitigation: Require explicit confirmation before write, approval, rejection, export, or shared-channel notification actions.

Risk: Manager tokens or elevated access could expose team-wide workforce information to employees.

Mitigation: Use employee tokens for employee-scoped queries and verify role mapping before accessing manager or admin endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brianppetty/skills/farmos-workforce)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown responses with optional shell commands and API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include employee counts, date-bounded time entry results, schedule or request status, certification alerts, and explicit error reporting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
