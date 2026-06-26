## Description: <br>
Budget Tracker helps an agent record local income and expense entries, list recent transactions, and produce a basic financial summary from a local ledger. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill for lightweight personal or project finance logging, recent transaction review, and basic local ledger summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation overstates budget and monthly report features, so financial summaries may be incomplete or misleading. <br>
Mitigation: Use the skill for lightweight local logging only, verify reports against the ledger, and do not rely on it for accounting or financial decisions. <br>
Risk: Income, expense categories, and notes are stored locally in a plain JSON ledger under the user's home directory. <br>
Mitigation: Avoid entering secrets or sensitive account details in transaction notes and apply local file protections appropriate for personal finance data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/budget-tracker) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local JSON ledger at $HOME/.budget-tracker/ledger.json.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
