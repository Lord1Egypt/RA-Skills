## Description:

Screens Chinese A-share stocks for short-term trading candidates using market sentiment, sector activity, price patterns, and fund flows, with proposed entry, stop-loss, and exit levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjjch](https://clawhub.ai/user/bjjch)

### License/Terms of Use:

MIT-0

## Use Case:

A-share traders and analysts use this skill to screen short-term candidates, check market conditions and trading risks, and prepare watchlists with position sizing and next-day review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External market data may be inaccurate, delayed, or unavailable, including plaintext LHB API data.

Mitigation: Cross-check prices and signals against trusted sources; do not use unverified data alone to make trades.

Risk: Short-term trading suggestions may lead to financial losses.

Mitigation: Treat candidate lists as analysis only; independently assess suitability, risk limits, and stop-loss levels.

Risk: Running the workflow may invoke other local trading skills and store alerts, journals, or reviews on disk.

Mitigation: Review linked skills before running them and protect or delete locally stored trading records as appropriate.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bjjch/skills/a-share-stock-radar)
- [Stock radar workflow](references/stock-radar.md)
- [Trading playbook](references/playbook.md)
- [Market sentiment cycle](references/emotion-cycle.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown watchlists and trading analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local alerts, trade journals, and review files when used.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
