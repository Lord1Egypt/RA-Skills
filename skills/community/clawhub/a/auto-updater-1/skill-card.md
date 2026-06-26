## Description: <br>
Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tigertamvip](https://clawhub.ai/user/tigertamvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to configure daily automated update checks for Clawdbot and installed ClawHub skills, then receive concise summaries of updates and failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily automated updates can change Clawdbot and installed skills without a clear approval gate. <br>
Mitigation: Use notify-only or dry-run mode where possible, pin trusted skills or versions, review changelogs before applying updates, and avoid enabling broad unattended daily updates unless that maintenance posture is intentional. <br>
Risk: The updater runs recurring commands that need write access to bot and skill directories. <br>
Mitigation: Run it under the intended user account, keep permissions narrow, review update summaries, and disable or remove the cron job if unexpected changes or failures appear. <br>


## Reference(s): <br>
- [Auto Updater 1 on ClawHub](https://clawhub.ai/tigertamvip/auto-updater-1) <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and cron configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance, optional update-script content, cron configuration, and human-readable update summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
