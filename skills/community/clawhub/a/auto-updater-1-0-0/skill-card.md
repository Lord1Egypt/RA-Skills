## Description: <br>
Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pntrivedy](https://clawhub.ai/user/pntrivedy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to configure unattended daily updates for Clawdbot and installed skills, then receive a concise summary of changed versions and any update failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended daily updates can change Clawdbot or installed skills without manual review. <br>
Mitigation: Review the cron entry and helper script before enabling automatic updates, and consider pinning or limiting update sources. <br>
Risk: An update failure or incompatible package change may leave the local setup in a broken state. <br>
Mitigation: Keep backups or rollback steps available and review delivered update summaries for failures. <br>
Risk: Detailed update summaries may expose local package or skill metadata if delivered through third-party notification services. <br>
Mitigation: Use delivery channels that are acceptable for this metadata, or reduce the detail included in notifications. <br>


## Reference(s): <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>
- [ClawHub skill page](https://clawhub.ai/pntrivedy/auto-updater-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include cron configuration, update command output summaries, version changes, and error notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
