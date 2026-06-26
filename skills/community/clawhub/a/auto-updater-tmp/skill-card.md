## Description: <br>
Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelaner](https://clawhub.ai/user/kelaner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Clawdbot operators use this skill to configure recurring update checks for Clawdbot and installed skills, then receive concise summaries of changes and failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring unattended updates can change Clawdbot and installed skills without review. <br>
Mitigation: Configure check-and-notify behavior, require review before applying updates, or restrict automatic updates to trusted sources. <br>
Risk: Updates may introduce regressions or incompatibilities across the bot or skill set. <br>
Mitigation: Pin versions where stability matters, keep backups, and maintain a documented rollback procedure before enabling scheduled updates. <br>
Risk: A scheduled job may continue applying changes after operational needs change. <br>
Mitigation: Document how to pause, disable, or remove the cron job and review the schedule periodically. <br>


## Reference(s): <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cron setup guidance and update summary message formats for agent execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
