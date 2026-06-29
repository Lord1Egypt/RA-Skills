## Description: <br>
Queries Feishu attendance data for the Basic Business Development Department and generates reports on team average hours, employees below 9.5 monthly average hours, and missing clock records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized HR, operations, or management users can use this skill to retrieve attendance records for configured teams and review monthly work-hour and missing-clock reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds a Feishu app secret. <br>
Mitigation: Remove the embedded secret, rotate the credential, and load future credentials from a secure environment or secret manager. <br>
Risk: The skill can retrieve sensitive employee attendance records without an authorization boundary. <br>
Mitigation: Install only for internal authorized HR or management users, document the Feishu API permissions, and restrict access to users allowed to view attendance data. <br>
Risk: The script uses hardcoded employee IDs and team lists that can become stale. <br>
Mitigation: Review and update the configured employee and department lists before relying on generated attendance reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runkecheng/attendance-check) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu attendance statistics query endpoint](https://open.feishu.cn/open-apis/attendance/v1/user_stats_datas/query?employee_type=employee_id) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text reports and markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include team average-hour rankings, employees below a monthly average-hour threshold, and missing clock-in or clock-out records.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
