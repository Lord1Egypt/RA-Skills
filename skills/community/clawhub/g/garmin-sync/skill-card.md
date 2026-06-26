## Description: <br>
Synchronizes Garmin Connect China daily health data by using browser automation to extract metrics such as steps, heart rate, sleep, stress, and body battery, then writes the results to configured databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[y634194250](https://clawhub.ai/user/y634194250) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and automation agents use this skill to collect Garmin Connect China daily health metrics and update local or server-side SQLite records. It is intended for accounts, browser profiles, databases, and remotes the user owns or is authorized to operate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports embedded account credentials and broad access to browser sessions, health databases, and remote pushes. <br>
Mitigation: Remove embedded credentials, use an explicit user-approved authentication flow, and run only in an environment where the user owns the Garmin account, browser profile, databases, and git remotes. <br>
Risk: The skill can write personal health data to local and server databases and push changes remotely. <br>
Mitigation: Make storage and remote destinations configurable, review extracted data before writing, and require confirmation before database writes or remote pushes. <br>


## Reference(s): <br>
- [Garmin Connect daily summary extraction reference](references/data-extraction.md) <br>
- [Garmin Connect China daily summary](https://connect.garmin.cn/app/daily-summary/10037590?date=YYYY-MM-DD) <br>
- [Garmin Connect China sign in](https://connect.garmin.cn/signin) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown instructions with browser automation snippets, Python commands, SQL schema notes, and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for extracting Garmin health metrics and updating SQLite databases.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
