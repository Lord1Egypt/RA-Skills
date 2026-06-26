## Description: <br>
Expense Tracker Pro tracks expenses via natural language, provides spending summaries, and helps users set budgets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhillin8](https://clawhub.ai/user/jhillin8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to log local expenses in natural language, automatically categorize spending, check budgets, and request spending summaries or CSV exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Expense and budget details may persist in local Clawd memory. <br>
Mitigation: Avoid recording highly sensitive financial details unless the user is comfortable managing that local data. <br>
Risk: CSV exports may create local files containing spending data. <br>
Mitigation: Review where exported files are stored and remove or protect them according to the user's privacy needs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Natural-language responses, spending summaries, budget status reports, and optional CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores expense and budget details locally in Clawd memory according to the artifact and security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
