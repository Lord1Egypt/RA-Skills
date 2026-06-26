## Description: <br>
Enhanced auto-updater with detailed logging, missed run recovery, and Gateway restart protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newolf20000](https://clawhub.ai/user/newolf20000) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Clawdbot users and operators use this skill to schedule recurring updates for Clawdbot and installed skills, with logging and summary reports for routine maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring automation can update the core agent and installed skills without per-update review. <br>
Mitigation: Start with dry-run or notification-only checks, review major skill changes before applying them, and keep a rollback path or backups for the agent and skill directories. <br>
Risk: Missed-run recovery can trigger updates after downtime when the user is not expecting immediate changes. <br>
Mitigation: Disable missed-run catch-up when surprise updates are undesirable and schedule updates during low-activity maintenance windows. <br>


## Reference(s): <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cron setup guidance, update commands, log paths, and report formatting examples.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
