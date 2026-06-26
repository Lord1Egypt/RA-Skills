## Description: <br>
Automatically update Clawdbot and all installed skills once daily, report what changed, and surface update errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicoataiza](https://clawhub.ai/user/nicoataiza) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to configure scheduled daily updates for Clawdbot and installed skills, then receive a concise summary of version changes and errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables unattended daily changes to Clawdbot and all installed skills. <br>
Mitigation: Start with dry-run checks, review updates before enabling automatic application, and confirm the cron removal command is available. <br>
Risk: An automatic update may break a local setup or introduce unexpected behavior. <br>
Mitigation: Pin or limit trusted update sources where possible and review the delivered update summary after each run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicoataiza/auto-updater-bak-2026-01-28t18-01-13-10-30) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cron setup guidance, update commands, dry-run checks, and human-readable update summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
