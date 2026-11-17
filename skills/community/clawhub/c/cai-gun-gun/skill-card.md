## Description:

Cai Gun Gun is a personal finance tracking skill that helps an agent record transactions, infer categories, manage account balances, import and export Excel bills, and summarize spending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmmg55](https://clawhub.ai/user/gmmg55)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage personal finance records through an agent, including adding income and expenses, checking account balances, importing third-party Excel bills, exporting records, and reviewing spending summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive transaction history, balances, merchants, notes, and configuration in both the user's home data directory and the skill data directory.

Mitigation: Install only when this storage behavior is acceptable, restrict access to both locations, and treat exported Excel files as sensitive.

Risk: Imported spreadsheets are merged into existing finance data and may contain untrusted or incorrect records.

Mitigation: Import only trusted spreadsheets, review import results, and export a backup before importing.

Risk: Delete and clear operations can remove finance records.

Mitigation: Confirm destructive actions explicitly before execution and use the required confirmation flag for full data clearing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gmmg55/skills/cai-gun-gun)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown-style agent responses with shell command invocations and JSON or Excel finance data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON finance records under ~/.cai-gun-gun/data and maintain synchronized copies in the skill data directory.]

## Skill Version(s):

2.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
