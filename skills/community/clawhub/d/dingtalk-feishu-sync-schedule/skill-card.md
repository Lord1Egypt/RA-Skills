## Description:

Synchronizes DingTalk calendar events for the current week into a Feishu calendar, with setup guidance for credentials, authorization, token refresh, and scheduled runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alittlebao](https://clawhub.ai/user/alittlebao)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, or agents who use both DingTalk and Feishu can use this skill to configure and run one-way calendar synchronization for the next seven days. It helps maintain a Feishu calendar from DingTalk events while managing local credential files and refresh tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local configuration files store application secrets, access tokens, and refresh tokens.

Mitigation: Restrict permissions on ~/.dingtalk and ~/.feishu files, keep them out of shared logs or backups, and avoid running the skill as root.

Risk: The sync process can delete or replace Feishu calendar events during repeated runs.

Mitigation: Test manually with a backup or non-critical calendar before scheduling automated runs, and review whether matching title and start time could affect manually created events.

Risk: Logs can expose token fragments or detailed calendar data.

Mitigation: Remove token fragments and unnecessary calendar details from logs before retaining or sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alittlebao/skills/dingtalk-feishu-sync-schedule)
- [Publisher profile](https://clawhub.ai/user/alittlebao)
- [DingTalk Open Platform](https://open.dingtalk.com/)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration steps; scripts produce console logs and local JSON configuration updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime flow can call DingTalk and Feishu APIs, update local credential files, refresh Feishu tokens, and delete or recreate Feishu calendar events.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
