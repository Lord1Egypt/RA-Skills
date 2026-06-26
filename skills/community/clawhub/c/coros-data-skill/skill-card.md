## Description: <br>
查询高驰（COROS）运动手表的运动数据，并在用户询问 COROS 跑步记录时帮助获取指定日期范围内的跑步活动。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wurongle](https://clawhub.ai/user/wurongle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure COROS account access, query running activities over a date range, and summarize distance from returned activity records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill logs in with COROS account credentials and can read running history, which may include personal fitness data. <br>
Mitigation: Install and run it only in trusted environments where access to the COROS account and activity history is acceptable. <br>
Risk: COROS_ACCOUNT, COROS_PASSWORD, and the generated MD5 password value can act as secrets if exposed. <br>
Mitigation: Keep scripts/.env private, avoid committing or sharing it, avoid logging the MD5 password value, and rotate the COROS password if the value is exposed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/wurongle/coros-data-skill) <br>
- [COROS training activity portal](https://trainingcn.coros.com/admin/views/activities) <br>
- [COROS account login API](https://teamcnapi.coros.com/account/login) <br>
- [COROS activity query API](https://teamcnapi.coros.com/activity/query) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with JavaScript code examples and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires COROS_ACCOUNT and COROS_PASSWORD secrets; activity data is returned only when the configured COROS account is used to execute the JavaScript client.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
