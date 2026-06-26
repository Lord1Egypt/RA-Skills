## Description: <br>
Track daily expenses in structured monthly markdown files with categories, tags, summaries, and spending analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aholake](https://clawhub.ai/user/aholake) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to log personal spending, generate monthly summaries, and review category-level spending patterns in a local workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes personal spending records to local markdown files, which may contain sensitive financial or contextual details. <br>
Mitigation: Keep entries free of sensitive details, review generated files for accuracy, and store the workspace in a trusted location. <br>
Risk: Broad spending examples may cause an agent to log casual spending comments when the user did not intend persistent tracking. <br>
Mitigation: Use explicit requests such as 'log this expense' before creating entries. <br>
Risk: Custom workspace, date, or month values can direct writes or reads to unexpected locations or periods. <br>
Mitigation: Use default paths and current dates unless the user explicitly provides trusted values. <br>


## Reference(s): <br>
- [Expense Categories](references/categories.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aholake/aholake-expense-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, terminal text, and optional JSON summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local monthly expense files under an expenses directory and can emit category summaries for a month.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
