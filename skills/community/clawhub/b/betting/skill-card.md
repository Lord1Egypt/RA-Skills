## Description:

Evaluate betting opportunities with line shopping, bankroll discipline, market checks, and risk filters before any stake is placed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to evaluate sports bets, props, parlays, exchanges, and prediction-style tickets with price math, market checks, bankroll discipline, and responsible-use boundaries before deciding whether to pass, wait, reduce size, or proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce betting analysis that users may mistake for legal, financial, gambling-compliance, or personalized suitability advice.

Mitigation: Keep outputs informational, avoid certainty or income framing, and stop at general information when legality, age, jurisdiction, or operator compliance is unclear.

Risk: Local betting notes under ~/betting/ may accumulate sensitive account, financial, or personal details if used carelessly.

Mitigation: Store only practical betting preferences and ticket notes, review the files periodically, and avoid credentials, account balances, payment details, wallet recovery phrases, and KYC data.

Risk: Stale odds, unmatched settlement rules, poor liquidity, correlation, or latency can make a ticket memo misleading.

Mitigation: Require exact market details, timestamps, settlement rules, limits or liquidity, and kill conditions before producing any analytical sizing guidance.

## Reference(s):

- [ClawHub Betting skill page](https://clawhub.ai/ivangdavila/skills/betting)
- [Skill homepage](https://clawic.com/skills/betting)
- [Clean Ticket Protocol](artifact/workflow.md)
- [Sizing and Price Math](artifact/sizing.md)
- [Market Checks](artifact/market-checks.md)
- [Red Flags](artifact/red-flags.md)
- [Ticket Memo Template](artifact/ticket-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown betting analysis memo with probability math, market checks, decision labels, and setup guidance when local notes are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local user preferences, ticket notes, market observations, and archives under ~/betting/ when the user wants tracking]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
