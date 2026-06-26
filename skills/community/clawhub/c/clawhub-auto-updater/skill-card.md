## Description: <br>
Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kendrick-lu](https://clawhub.ai/user/kendrick-lu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to configure daily cron-based checks that update Clawdbot and installed skills, then receive a concise update summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic updates can change the agent environment before each individual update is reviewed. <br>
Mitigation: Run `clawdhub update --all --dry-run` first in critical setups and manually review or pin important skills where possible. <br>
Risk: A scheduled update may introduce an operational issue or unwanted change. <br>
Mitigation: Keep the cron job removable with `clawdbot cron remove "Daily Auto-Update"` and monitor delivered update summaries for errors. <br>


## Reference(s): <br>
- [ClawHub Auto Updater](https://clawhub.ai/kendrick-lu/clawhub-auto-updater) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance, cron configuration, troubleshooting steps, and update-summary message formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
