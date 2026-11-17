## Description:

Track and maximize credit card benefits (monthly, quarterly, yearly). Manage cards, log benefit usage, get reminders for expiring perks, see ROI summaries, and optimize spending categories for maximum rewards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[softtrymee](https://clawhub.ai/user/softtrymee)

### License/Terms of Use:


## Use Case:

External users use this agent skill to maintain a local record of credit card benefits, usage, renewal timing, and reward categories so they can capture expiring perks and evaluate annual fee ROI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and updates a local financial profile, including card ownership, benefit usage, dates, fees, and reward preferences.

Mitigation: Review the skill before installation and avoid adding sensitive account numbers or credentials to card, benefit, or notes fields.

Risk: The tracking command can read or replace JSON files outside the data folder when given unsafe tracking-period values.

Mitigation: Validate tracking periods strictly as YYYY_MM before running tracking commands, and fix path handling before deploying the skill for regular use.

Risk: Benefit and cashback details discovered through web search may be outdated or inaccurate.

Mitigation: Confirm benefit amounts, frequencies, activation requirements, and cashback rates with the user or authoritative card issuer sources before saving them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/softtrymee/skills/card-benefits-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/softtrymee)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summaries, JSON command results, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may summarize local card, benefit, usage, renewal, and reward-category data.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
