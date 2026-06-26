## Description: <br>
Trust-based budget system for multi-agent teams with daily token limits, budget threshold alerts, audit logging, and advisory mesh privilege revocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators of OpenClaw-style multi-agent systems use this skill to track daily agent token budgets, surface warning and over-budget states, and maintain governance logs for follow-up action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be interpreted as hard enforcement for spawn privileges even though the security evidence says enforcement is not proven. <br>
Mitigation: Treat the skill as an advisory local auditor until privilege revocation is independently confirmed in the target environment. <br>
Risk: The audit script can persistently rewrite agent budget and governance state. <br>
Mitigation: Back up BUDGET.json and governance log files, verify the expected schema, and test recovery before enabling routine use. <br>
Risk: Automated scheduling could repeatedly apply changes without dry-run or rollback controls. <br>
Mitigation: Do not schedule the audit automatically until a dry-run path, rollback plan, and timezone assumptions have been validated. <br>


## Reference(s): <br>
- [Agent Governance Framework](references/GOVERNANCE.md) <br>
- [ClawHub skill page](https://clawhub.ai/nissan/agent-budget-governance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled audit script can emit human-readable text or JSON reports and update local governance files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file operations only; requires python3 and no environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
