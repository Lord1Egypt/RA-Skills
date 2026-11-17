## Description:

Debt Blitz Planner compares avalanche, snowball, and minimum-only debt payoff strategies using month-by-month amortization math to show debt-free dates, total interest, savings, and payoff schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to compare personal consumer-debt payoff plans, decide which debt to prioritize, model extra-payment or fixed-budget scenarios, and export payoff schedules for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV exports may contain sensitive personal financial labels and payoff data.

Mitigation: Save exports only to trusted local paths and avoid sharing generated CSV files unless the financial labels and amounts are intended for disclosure.

Risk: Debt names beginning with spreadsheet formula characters can create formula-injection risk when CSV exports are opened in spreadsheet software.

Mitigation: Sanitize debt names that start with characters such as =, +, -, or @ before generating or opening CSV exports.

Risk: Attacker-provided debt names can affect report or export contents.

Mitigation: Use user-confirmed debt labels and review generated text, JSON, or CSV output before relying on or distributing it.

## Reference(s):

- [Debt Payoff Math - Reference](references/payoff-math.md)
- [ClawHub skill page](https://clawhub.ai/voronindenis5/skills/debt-blitz-planner)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, JSON, CSV]

**Output Format:** [Markdown guidance with inline shell commands; the bundled planner can also emit plain text reports, JSON summaries, or CSV schedule files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python 3.9+ and standard-library dependencies; no API keys or network services are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
