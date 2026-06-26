## Description: <br>
Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to configure scheduled maintenance that updates Clawdbot and installed skills, then reports what changed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled automatic updates can change Clawdbot and installed skills before each update is reviewed. <br>
Mitigation: Run dry-run checks first, review updates before applying them, avoid elevated permissions, and confirm the cron job can be disabled with `clawdbot cron remove "Daily Auto-Update"`. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andy27725/auto-updater-andy27725) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup commands, update procedures, and summary-message guidance for scheduled Clawdbot and skill updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
