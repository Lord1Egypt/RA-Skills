## Description:

Garmin Sync CN helps an agent synchronize same-day Garmin Connect CN health data by using browser automation to extract metrics such as steps, heart rate, sleep, stress, and body battery, then update configured local and server databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y634194250](https://clawhub.ai/user/y634194250)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who control the Garmin account, browser profile, databases, server, and git remotes use this skill to collect daily Garmin Connect CN wellness metrics and synchronize them into an existing health-data workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact contains an embedded Garmin account password.

Mitigation: Treat the password as compromised, rotate it before use, and replace hardcoded credentials with a secret manager or interactive login flow.

Risk: The workflow accesses private health data and may publish database changes through git.

Mitigation: Use only allowlisted destinations, avoid committing health databases to git history, and confirm the data minimization and retention policy before synchronization.

Risk: Reusing a broad browser session can expose more account access than the skill needs.

Mitigation: Use a dedicated browser profile for Garmin Connect CN and require explicit confirmation before navigating, extracting data, or reusing a session.

Risk: Privileged local and server database writes can damage or leak health records if paths are wrong.

Mitigation: Run with least privilege, back up databases, and verify local and server paths before executing write operations.

## Reference(s):

- [Garmin Connect CN Daily Summary Data Extraction Reference](artifact/references/data-extraction.md)
- [Garmin Sync CN on ClawHub](https://clawhub.ai/y634194250/skills/garmin-sync)
- [Garmin Connect CN Daily Summary](https://connect.garmin.cn/app/daily-summary/10037590?date=YYYY-MM-DD)
- [Garmin Connect CN Sign In](https://connect.garmin.cn/signin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, Python, SQL, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-controlled account access, browser profile state, database paths, server destination, and git remotes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
