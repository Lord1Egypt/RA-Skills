## Description: <br>
Analyst Watchdog monitors a local API scoreboard, detects milestones and promotions, and writes markdown findings and file-based alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a local watchdog that monitors model evaluation scoreboard data, records milestones and anomalies, and hands off file-based alerts to an orchestrator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background scheduling can repeatedly poll local services and write alert files without human review. <br>
Mitigation: Confirm any cron, LaunchAgent, or orchestrator setup before deployment and run the skill only in the intended workspace. <br>
Risk: ALERT_TELEGRAM.md can be consumed by separate automation that sends messages externally. <br>
Mitigation: Review downstream alert handlers and credentials before enabling external notification delivery; this skill itself only writes local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/analyst-watchdog) <br>
- [Publisher profile](https://clawhub.ai/user/nissan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown files, JSON state, and terminal log text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local FINDINGS.md, OUTBOX.md, ALERT_TELEGRAM.md, and state files; reads from localhost and does not require outbound network access.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
