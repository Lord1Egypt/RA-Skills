## Description: <br>
BigFocus tracks product prices, public figure updates, industry information, and custom indicators, then reports changes through scheduled checks and user-facing tracking summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kobenfang](https://clawhub.ai/user/kobenfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and teams use this skill to maintain a personal watchlist for prices, public updates, industry topics, and numeric indicators, with confirmation before tracker changes and scheduled reporting when monitored values change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist trackers and raw tracking history in local workspace memory files. <br>
Mitigation: Review stored tracker targets and history regularly, and avoid tracking sensitive personal or confidential information. <br>
Risk: Scheduled scans may contact external sites or public APIs for tracked products and indicators. <br>
Mitigation: Review or restrict allowed URLs and domains before enabling recurring checks. <br>
Risk: Cron notifications can send tracking updates to configured channels or recipients. <br>
Mitigation: Confirm the destination channel and recipient before enabling cron notifications. <br>
Risk: Tracker additions, deletions, and status changes affect persistent monitoring behavior. <br>
Mitigation: Require explicit user confirmation before adding, deleting, pausing, resuming, or changing tracker intervals. <br>


## Reference(s): <br>
- [BigFocus Cron Install Template](references/cron-install-shell.sh) <br>
- [BigFocus Cron Templates](references/cron-templates.json) <br>
- [BigFocus ClawHub Skill Page](https://clawhub.ai/kobenfang/skills/bigfocus) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown tracking reports and confirmations, JSON command results, and shell commands for cron setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist tracker state and raw history in workspace memory files and may issue scheduled checks for active trackers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
