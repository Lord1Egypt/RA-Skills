## Description:

Returns blackjack basic-strategy actions for player cards and dealer upcard under 6-deck S17 rules, with JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can ask an agent for blackjack basic-strategy decisions for a stated player hand and dealer upcard. The skill is intended for rule-specific advisory output, not for card counting or casino-rule discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install metadata registers a recurring annual automaton even though the advisor itself is a local calculator.

Mitigation: Review the managed automaton and cron schedule before installation; remove or disable the schedule unless unattended annual execution is intended.

Risk: Advice is only appropriate for the blackjack rules stated by the artifact.

Mitigation: Confirm the table rules match 6 decks, dealer stands on soft 17, double after split, and late surrender before relying on the recommendation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mibayy/skills/casino-blackjack-advisor)
- [Publisher Profile](https://clawhub.ai/user/mibayy)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object with action, explanation, hand type, total, and confidence fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external dependencies; assumes 6-deck S17 blackjack with double after split and late surrender.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
