## Description: <br>
Garmin Connect Skill helps OpenClaw agents authenticate with Garmin Connect, sync health and workout data from China or global accounts, and store it in SQLite for fast local querying. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tcyxk](https://clawhub.ai/user/tcyxk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect Garmin accounts, sync health metrics and workouts into a local SQLite database, and generate or send health summaries through OpenClaw, Feishu, or webhooks. <br>

### Deployment Geography for Use: <br>
Global, including Garmin China and Garmin global account regions. <br>

## Known Risks and Mitigations: <br>
Risk: Garmin credentials and session data are sensitive and may be stored locally. <br>
Mitigation: Review before installing, use only on a trusted machine, avoid entering Garmin passwords on the command line, and protect or delete ~/.garth/session.json when no longer needed. <br>
Risk: The skill stores health data and generated health reports locally. <br>
Mitigation: Protect or delete ~/.clawdbot health data when it is no longer needed, and limit local file access to trusted users and processes. <br>
Risk: Feishu, webhook, and timer features can send health data outside the local machine. <br>
Mitigation: Enable Feishu, webhook, and timer features only after confirming exactly what health data will be sent and where. <br>
Risk: Embedded Feishu credentials may be present in the artifact behavior reported by security evidence. <br>
Mitigation: Do not use embedded Feishu credentials; configure fresh credentials or webhooks under the user's own account and rotate any exposed secrets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tcyxk/garmin-connect-skill) <br>
- [README](artifact/README.md) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash and Python snippets; scripts may write SQLite, JSON, and text health-report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write local Garmin credential, health-data, Feishu, webhook, timer, and SQLite files depending on the enabled workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
