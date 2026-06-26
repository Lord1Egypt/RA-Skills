## Description: <br>
Automatically update Clawdbot and all installed skills once daily. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[make453](https://clawhub.ai/user/make453) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to configure scheduled update checks for Clawdbot and installed skills, then receive a concise summary of what changed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a persistent scheduled job that updates Clawdbot and every installed skill without per-update review. <br>
Mitigation: Use a notify-only or dry-run setup first, review proposed updates before applying them, and enable automatic updates only when broad scheduled changes are acceptable. <br>
Risk: Automatic updates may change critical skills or agent behavior unexpectedly. <br>
Mitigation: Pin or allowlist critical skills where possible and keep a rollback or manual update path for important environments. <br>
Risk: Users may forget that the daily update job remains active after setup. <br>
Mitigation: Confirm the cron job is visible in `clawdbot cron list` and keep the documented removal command available before enabling the schedule. <br>


## Reference(s): <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>
- [ClawHub Release Page](https://clawhub.ai/make453/auto-updater-bak2) <br>
- [Publisher Profile](https://clawhub.ai/user/make453) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose cron configuration and update-summary text for the user to review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
