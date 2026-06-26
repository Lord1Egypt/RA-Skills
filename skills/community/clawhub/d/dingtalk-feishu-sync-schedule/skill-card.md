## Description: <br>
Synchronizes DingTalk calendar events for today and the next six days into Feishu Calendar, with setup guidance, token refresh, and scheduled execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alittlebao](https://clawhub.ai/user/alittlebao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who use both DingTalk and Feishu calendars use this skill to configure local credentials, refresh Feishu tokens, and copy near-term DingTalk events into Feishu Calendar on demand or by cron. Agents can use it to guide setup, run the sync script, and troubleshoot token, calendar, and permission issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu event deletion can affect more calendar events than users may expect when an event has the sync marker or matches a DingTalk title and start time. <br>
Mitigation: Review or change the deletion logic before enabling cron so it deletes only events clearly created by this tool; test on a non-critical calendar first. <br>
Risk: The skill stores DingTalk and Feishu credentials, access tokens, and refresh tokens in local configuration files. <br>
Mitigation: Restrict file permissions, keep credentials out of shared workspaces and logs, and grant only the calendar permissions needed for the sync. <br>
Risk: Sync logs and command output may expose calendar titles, locations, timing, or operational details. <br>
Mitigation: Protect log files such as /var/log/dingtalk_sync.log and avoid forwarding logs to places where calendar details should not be visible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alittlebao/dingtalk-feishu-sync-schedule) <br>
- [DingTalk Open Platform](https://open.dingtalk.com/) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python execution steps, configuration file fields, and API endpoint notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON config files under ~/.dingtalk and ~/.feishu; may call DingTalk and Feishu calendar APIs when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
