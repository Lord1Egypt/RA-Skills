## Description:

Budgetly helps users set category budgets, log expenses, visualize spending limits, monitor subscriptions, and forecast spending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Budgetly to keep local records of expenses, balances, budget checks, trends, forecasts, alerts, and tax notes from the command line. It is suited for personal finance tracking where local plaintext storage and user-managed exports are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance, balance, and tax notes are stored as local plaintext files under ~/.local/share/budgetly.

Mitigation: Do not enter account numbers or highly sensitive tax details, and review local file permissions before use on shared systems.

Risk: CSV exports may contain personal finance data and can be risky to open directly in spreadsheet applications.

Mitigation: Inspect exported CSV content before opening it in spreadsheets and share exports only through trusted channels.

## Reference(s):

- [Budgetly ClawHub listing](https://clawhub.ai/ckchzh/skills/budgetly)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text command output with optional JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores finance logs and generated exports locally under ~/.local/share/budgetly.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
