## Description: <br>
ExpenseLog helps users record expenses conversationally, categorize spending, track budgets, generate monthly reports, and export CSV data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent log personal spending, summarize monthly totals by category, compare against budgets, and export CSV records for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Expense records can contain sensitive financial details and are stored locally on disk. <br>
Mitigation: Use the skill only in trusted workspaces, avoid entering unnecessary sensitive details on shared machines, and keep independent backups of important data. <br>
Risk: Ambiguous prompts may create unintended state-changing expense entries. <br>
Mitigation: Use explicit phrases such as "log this expense" when adding records and review logged entries before relying on reports or exports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/expense-log) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files] <br>
**Output Format:** [Plain text or Markdown summaries, JSON-like expense records, and CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores expense records in a local expenses.json file when used through the included JavaScript module.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
