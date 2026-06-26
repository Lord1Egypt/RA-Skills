## Description: <br>
Daily News Brief automatically gathers international affairs, economic, and technology news each morning and produces a structured Markdown brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zwang2sz](https://clawhub.ai/user/zwang2sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or external users who want a scheduled daily digest use this skill to collect, rank, archive, and optionally publish news across international affairs, economics, and technology. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended scheduled execution may continue fetching, saving, or publishing briefs after the user no longer expects it. <br>
Mitigation: Review the configured cron, Task Scheduler, or systemd entry before enabling automation, and remove the schedule when unattended execution is no longer wanted. <br>
Risk: Configured output channels and recipients may publish the generated brief to unintended destinations. <br>
Mitigation: Review config.json recipients and outputChannels before enabling publishing, and keep console-only output when testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zwang2sz/daily-news-brief) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefs, console text, setup commands, and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefs are saved to latest-brief.md and dated files under history/; configured channels can publish the same Markdown content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
