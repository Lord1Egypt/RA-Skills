## Description: <br>
Configures and troubleshoots a Bank of China forex monitor with per-currency thresholds, selected price columns, quiet hours, baseline comparison, deduplicated alerts, and optional OpenClaw notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiehuapeng](https://clawhub.ai/user/xiehuapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up, configure, and troubleshoot scheduled Bank of China forex monitoring with threshold-based alerts and optional OpenClaw message delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scheduled monitor can send external notifications to a configured channel and target. <br>
Mitigation: Confirm the OpenClaw channel, target, and account id before enabling notifications, and run the script manually once before scheduling it. <br>
Risk: Local .openclaw-state files can contain alert history and recipient identifiers. <br>
Mitigation: Keep .openclaw-state private and out of version control. <br>
Risk: A frequent cron schedule can repeatedly fetch Bank of China rate data and generate alerts. <br>
Mitigation: Review the cron schedule and threshold configuration before installation, and use quiet hours or higher thresholds when appropriate. <br>


## Reference(s): <br>
- [Configuration](references/configuration.md) <br>
- [Bank of China foreign exchange rates](https://www.boc.cn/sourcedb/whpj/) <br>
- [ClawHub release page](https://clawhub.ai/xiehuapeng/boc-forex-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and expected text status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The installed runner writes local JSON state under .openclaw-state and may send optional OpenClaw notifications when runtime notification parameters are configured.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
