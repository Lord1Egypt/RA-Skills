## Description: <br>
Process bank transaction CSV exports (Nordea, ICA), auto-categorize transactions using configurable rules, manage transaction links, and generate analytical database views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patello](https://clawhub.ai/user/patello) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to operate a local personal-finance CLI for importing bank CSV exports, maintaining categorization rules, linking transfers or reimbursements, and generating SQLite-backed financial summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads bank CSV exports and stores sensitive personal-finance data in a local SQLite database. <br>
Mitigation: Keep the database outside the skill directory with appropriate local access controls and back it up before imports or cleanup operations. <br>
Risk: Commands that clean up, link, delete, or recalculate records can change transaction history or adjusted amounts. <br>
Mitigation: Use dry-run options where available, review previews before applying changes, and require explicit confirmation or the documented --yes flag for destructive non-interactive runs. <br>
Risk: Automatic categorization and linking rules can misclassify transactions, transfers, or reimbursements. <br>
Mitigation: Preview rule matches, inspect uncategorized and non-zero adjusted transactions, and manually correct categories or links when reports look inconsistent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patello/skills/financial-categorizer) <br>
- [Publisher profile](https://clawhub.ai/user/patello) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQLite database paths, CLI flags, category names, match rules, account names, and dry-run or confirmation options supplied by the user.] <br>

## Skill Version(s): <br>
1.6.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
