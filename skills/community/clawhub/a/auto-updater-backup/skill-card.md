## Description: <br>
Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[make453](https://clawhub.ai/user/make453) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure an agent-managed daily update routine for Clawdbot and installed skills, then receive a concise update summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent unattended updates can replace Clawdbot and installed skills without a review step. <br>
Mitigation: Enable the cron job only when automatic updates are intended; prefer dry-runs or manual approval for higher-control environments. <br>
Risk: Updated skills or Clawdbot versions may introduce behavior changes or incompatibilities. <br>
Mitigation: Review changelogs, use trusted sources or version pinning where possible, and keep a rollback plan before enabling daily updates. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/make453/auto-updater-backup) <br>
- [Agent Implementation Guide](artifact/references/agent-guide.md) <br>
- [Update Summary Examples](artifact/references/summary-examples.md) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or configure persistent cron-based unattended updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
