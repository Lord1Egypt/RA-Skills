## Description: <br>
Automatically update Clawdbot and all installed skills once daily, using cron to check for updates, apply them, and message the user with a summary of what changed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninwonk](https://clawhub.ai/user/ninwonk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to configure daily unattended updates for Clawdbot and installed skills, then receive a concise update summary after each run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended daily updates can change Clawdbot and installed skills without interactive review. <br>
Mitigation: Use a dry run before enabling the schedule, and prefer manual or allowlisted updates for important workflows. <br>
Risk: The recurring cron job can continue applying updates after setup. <br>
Mitigation: Confirm the cron entry after installation and keep the removal command available if updates cause problems. <br>
Risk: Publisher or package confusion could cause users to install a skill they did not intend to trust. <br>
Mitigation: Verify the ClawHub publisher handle and package identity before enabling automatic updates. <br>


## Reference(s): <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May configure a daily cron job that performs unattended updates and reports results to the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
