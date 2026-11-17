## Description:

Use when an external event thesis needs market confirmation before commitment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and strategy researchers use this skill to ask an agent to evaluate whether Polymarket filled-trade history confirms an external catalyst before committing to a market strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence event-driven market strategy decisions, and its outputs may be mistaken for investment advice.

Mitigation: Treat outputs as research support only and require human review before any real-money trading action.

Risk: Generated NautilusTrader strategy code or configuration may be incomplete, overfit, or unsuitable for the user's engine constraints.

Mitigation: Review, test, and tune generated code or configuration against the target engine and historical data before deployment.

Risk: Catalyst confirmation can be misleading when information was priced in early, market mapping is weak, or a temporary spike does not persist.

Mitigation: Check market-to-catalyst fit, event timing, filled-trade history coverage, and reversal behavior before relying on the analysis.

## Reference(s):

- [Catalyst Confirmation ClawHub skill page](https://clawhub.ai/superior-ai/skills/catalyst-confirmation)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown with JSON configuration examples and strategy-generation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent output should be treated as research support, not investment advice or approval for real-money trading.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
