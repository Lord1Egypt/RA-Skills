## Description:

Expense Tracker Daily helps an OpenClaw agent record natural-language expense entries, categorize them, and summarize daily, weekly, or monthly spending using a local JSON ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glorysunshine](https://clawhub.ai/user/glorysunshine)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to track expenses from conversational input without opening a separate finance app. The agent extracts amount, category, description, and date, then calls the local CLI to add, list, delete, or summarize expense records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided expense descriptions may be placed into shell commands unsafely when an agent follows the current command-invocation guidance.

Mitigation: Pass dynamic values as separate process arguments, avoid shell interpolation, and reject descriptions containing shell syntax until command construction is hardened.

Risk: The skill stores personal expense data in a local JSON ledger in the user's home directory.

Mitigation: Install only when local ledger storage is acceptable and avoid recording sensitive details that are not needed for expense tracking.

## Reference(s):

- [Expense category keyword map](references/categories.md)
- [OpenClaw project](https://github.com/nicepkg/openclaw)
- [ClawHub skill page](https://clawhub.ai/glorysunshine/skills/expense-tracker-daily)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON]

**Output Format:** [Markdown responses with inline shell commands and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores expense records in a local JSON ledger under the user's home directory.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
