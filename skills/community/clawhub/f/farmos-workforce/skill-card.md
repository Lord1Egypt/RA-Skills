## Description: <br>
Query employee data, time clock entries, schedules, and requests with authentication that scopes employees to their own data and managers to their team. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianppetty](https://clawhub.ai/user/brianppetty) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Farm employees, managers, and admins use this skill to record time-clock activity, capture schedule changes and time-off requests, review team availability, approve requests, and prepare payroll exports within role-scoped access controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change sensitive employee workforce records, including clock actions, requests, approvals, rejections, and payroll exports. <br>
Mitigation: Install only in a trusted FarmOS environment and require explicit user confirmation before record-changing actions or payroll exports. <br>
Risk: Schedule details or personal reasons could be broadcast to an inappropriate audience. <br>
Mitigation: Verify role mappings, API permissions, and #farm-workforce membership, and avoid posting personal reasons beyond authorized managers. <br>
Risk: Using the wrong token could expose team-wide employee data to an employee-scoped request. <br>
Mitigation: Use role-appropriate authenticated tokens and confirm employee, manager, and admin access boundaries before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and HTTP API request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated FarmOS access and role-appropriate tokens for protected employee, time, request, calendar, skills, and payroll endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
