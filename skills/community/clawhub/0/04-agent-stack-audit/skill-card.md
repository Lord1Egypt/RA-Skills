## Description: <br>
Monthly health check for an agent stack that audits crons, scripts, API keys, skills, memory files, tools, and subscriptions, then produces a ranked cleanup brief for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pingukim225](https://clawhub.ai/user/pingukim225) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent-stack maintainers use this skill to identify unused, redundant, outdated, or risky automation assets and decide what to clean up. It is intended for recurring maintenance when automation reliability drops, costs increase, or scheduled jobs and API usage need review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require broad visibility into automation directories, scheduled tasks, API inventories, subscriptions, and memory files. <br>
Mitigation: Define the exact in-scope directories, cron sources, accounts, API inventories, subscription records, and memory files before running it. <br>
Risk: Audit output may expose secrets or sensitive operational details from API keys, subscription records, or memory files. <br>
Mitigation: Require secrets and sensitive account details to be masked in reports before sharing or storing the output. <br>
Risk: The skill includes a narrow script-editing exception for confirmed dead API calls. <br>
Mitigation: Do not permit cleanup or script edits unless you explicitly approve a diff and have a rollback path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pingukim225/04-agent-stack-audit) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown audit reports with ranked findings, classification tables, recommended actions, and optional cleanup summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces state/stack_audit_YYYY-MM-DD.md for full audits and state/cron_health_YYYY-MM-DD.md for quick cron health scans.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
