## Description: <br>
Personal bookkeeping assistant for local income and expense tracking, monthly reports with comparisons, budget alerts, and savings goal management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Beancount to record local personal finance transactions, review monthly income and expense reports, manage budgets, and track savings goals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal finance records are stored in local files under ~/.bookkeeping. <br>
Mitigation: Use the skill only on trusted machines and protect, back up, or remove those local files according to the user's data handling needs. <br>
Risk: The auxiliary scripts/script.sh can write command activity to ~/.local/share/beancount/history.log. <br>
Mitigation: Prefer the documented scripts/book.sh commands; if scripts/script.sh is used, review the local history log and remove it when no longer needed. <br>


## Reference(s): <br>
- [Beancount on ClawHub](https://clawhub.ai/bytesagain-lab/beancount) <br>
- [Bookkeeping Tips](tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local JSON file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores bookkeeping records, budgets, and goals in local JSON files under ~/.bookkeeping.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
