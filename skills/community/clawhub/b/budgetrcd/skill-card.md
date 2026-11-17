## Description:

BudgetRcd helps agents record expenses, set budgets, check remaining balances, track savings goals, and adjust weekday/weekend budget planning with carry-forward calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kazuya-ecnu](https://clawhub.ai/user/kazuya-ecnu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal finance agents use this skill to maintain local budget records, add receipts or expense entries, inspect month/day spending, and compute remaining budget by weekday and weekend rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles personal finance records and local receipt files.

Mitigation: Use it only in a trusted local environment and avoid passing arbitrary or sensitive receipt image paths.

Risk: Weak path validation can allow writes or receipt copies outside the intended budget area.

Mitigation: Restrict operations to a fixed budget root and validate all source and destination paths before installing or running the skill.

Risk: Sensitive edits and deletes may not reliably enforce user confirmation.

Mitigation: Require explicit confirmation before update or delete operations and audit those functions before relying on them.

Risk: Weak date and filename validation can create malformed records or unsafe receipt filenames.

Mitigation: Validate dates, categories, amounts, and generated image filenames before writing records or copying files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kazuya-ecnu/skills/budgetrcd)

## Skill Output:

**Output Type(s):** [Text, Files, Configuration]

**Output Format:** [Conversational budget summaries plus JSON expense, budget, and configuration records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and writes local budget data and may copy receipt images.]

## Skill Version(s):

1.5.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
