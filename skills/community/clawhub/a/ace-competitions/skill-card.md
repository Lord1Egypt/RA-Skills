## Description: <br>
Ace competitions agent workflow - search, enter, track competitions. Uses browser automation for form filling, email verification, and competition entry. Integrates with competitions dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefanferreira](https://clawhub.ai/user/stefanferreira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to discover online competitions, prepare and submit entries through browser automation, verify entries, and track competition status in a dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may submit real competition entries and complete verification workflows using contact details. <br>
Mitigation: Require human approval before each submission and verification step, and use only dedicated competition email and phone credentials. <br>
Risk: Competition tracking can expose personal data, screenshots, logs, dashboard records, and backups. <br>
Mitigation: Restrict dashboard and API access, and define retention and deletion rules for screenshots, logs, backups, and personal data before use. <br>
Risk: Scheduled automation can run repeated searches, verification checks, and dashboard updates without ongoing operator review. <br>
Mitigation: Review the cron schedule and referenced helper scripts before installation, and keep scheduled jobs disabled until the operator confirms the workflow boundaries. <br>


## Reference(s): <br>
- [Ace Competitions ClawHub listing](https://clawhub.ai/stefanferreira/ace-competitions) <br>
- [Publisher profile](https://clawhub.ai/user/stefanferreira) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline bash, Python, SQL, JSON, and cron examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dashboard records, screenshots, verification tasks, and entry status updates when used with the referenced local automation components.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
