## Description: <br>
Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kellanlab](https://clawhub.ai/user/kellanlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to configure a scheduled updater that keeps Clawdbot and installed skills current and reports what changed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A recurring update job can change Clawdbot and installed skills without per-update review. <br>
Mitigation: Install only when automatic updates are intended, run documented dry-run or manual checks first, and keep the Daily Auto-Update cron job easy to remove. <br>
Risk: An automatic update may break a local setup or pull changes from sources the user has not reviewed. <br>
Mitigation: Restrict updates to trusted sources where possible, review the delivered update summary, and use manual update commands when failures or unexpected changes appear. <br>


## Reference(s): <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/kellanlab/auto-updater-bak) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and cron configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scheduled update setup guidance and concise update summaries for the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
