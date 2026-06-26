## Description: <br>
Garmin Connect integration for OpenClaw that syncs fitness data including steps, heart rate, calories, workouts, and sleep through OAuth into local SQLite storage for fast access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tcyxk](https://clawhub.ai/user/tcyxk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to authenticate with Garmin Connect, synchronize Garmin health and workout data, and query local SQLite-backed summaries for conversational health status, sleep, activity, and workout reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Garmin credentials and session material are sensitive and the security guidance warns against password-on-command-line examples. <br>
Mitigation: Avoid command-line password entry when possible, restrict access to ~/.garth/session.json, and rotate Garmin credentials if exposure is suspected. <br>
Risk: Local SQLite and cache files may contain sensitive Garmin health and activity data. <br>
Mitigation: Protect ~/.clawdbot/garmin/data.db and related cache files with least-privilege permissions, encrypted storage where available, and careful backup handling. <br>
Risk: Feishu and webhook report scripts can send sensitive health summaries to external destinations. <br>
Mitigation: Review outbound report configuration, remove or rotate embedded Feishu credentials, and disable Feishu/webhook reporting unless the destination is intended. <br>
Risk: Daemon, timer, or scheduled sync behavior can repeatedly collect or share data after installation. <br>
Mitigation: Review the daemon and timer setup before enabling it, and disable background sync or outbound reports when continuous operation is not required. <br>


## Reference(s): <br>
- [ClawHub Garmin Connect release page](https://clawhub.ai/tcyxk/garmin-connect-tcyxk) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python examples, and text health summaries backed by local SQLite data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or update local Garmin session files, SQLite health data, sync status, and optional outbound report configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
