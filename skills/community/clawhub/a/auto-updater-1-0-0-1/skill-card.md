## Description: <br>
Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gwsq](https://clawhub.ai/user/Gwsq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to configure scheduled updates for Clawdbot and installed skills, then receive concise update summaries with any failures or follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill automates broad unattended updates to Clawdbot and all installed skills. <br>
Mitigation: Install only when unattended updates are intended; prefer manual or notify-only updates, pin trusted versions where possible, and review update summaries before applying broad changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Gwsq/auto-updater-1-0-0-1) <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps, cron commands, optional update scripts, troubleshooting guidance, and human-readable update summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version, artifact metadata.version, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
