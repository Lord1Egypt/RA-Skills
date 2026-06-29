## Description: <br>
基于明日DMP开放平台API，帮助用户获取广告账户、创建人群同步任务并查询同步状态，用于将DMP人群包同步到广告平台进行投放。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingri26](https://clawhub.ai/user/mingri26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators and developers use this skill to synchronize Mingdata DMP audience packages to supported advertising platforms, then check account lists and task status. It is intended for audience activation workflows that require API credentials, explicit parameter confirmation, and review of data authorization obligations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive Mingdata DMP Access Key and Secret Key could be exposed if provided directly in chat. <br>
Mitigation: Use a credential store or out-of-band secret setup, and do not paste AK/SK values into chat. <br>
Risk: The skill depends on separately installed auth and logger skills, and the artifact scans local skill directories before executing the discovered auth script. <br>
Mitigation: Install only trusted versions of the dependency skills and prefer a release that pins the auth dependency to a verified path. <br>
Risk: Task logging may record task IDs and synchronization parameters that could be sensitive for campaign operations. <br>
Mitigation: Review what the logger records before enabling it, and skip or disable logging when recorded fields exceed internal policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mingri26/dmp-audience-sync) <br>
- [Mingdata DMP auth skill](https://clawhub.ai/mingri26/mingdata-dmp-auth) <br>
- [DMP task logger skill](https://clawhub.ai/mingri26/dmp-skill-logger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API/script responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Mingdata DMP API credentials and the separate mingdata-dmp-auth skill; task logging is optional through skill-logger.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
