## Description: <br>
Cron Setup Guide Free helps agents configure Agent Gateway scheduled jobs across one-time, interval, and cron schedules, session modes, delivery settings, and basic job management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through creating and managing Agent Gateway scheduled jobs, including schedule selection, session mode selection, delivery configuration, and basic job lifecycle commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to configure persistent scheduled jobs. <br>
Mitigation: Use it only for explicit cron setup requests and confirm the exact schedule and command before running any job creation or edit command. <br>
Risk: Announce delivery can send results to external Telegram or Discord destinations. <br>
Mitigation: Verify the channel and recipient before enabling announce delivery. <br>
Risk: Delete-after-run behavior can remove scheduled jobs after execution. <br>
Mitigation: Confirm delete-after-run is intended before including it in a proposed command or configuration. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent scheduled jobs and external delivery destinations that require user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
