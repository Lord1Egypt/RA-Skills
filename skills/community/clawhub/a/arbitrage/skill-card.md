## Description:

Find, validate, and compare arbitrage opportunities across markets with fee-aware math, execution sequencing, and failure-mode checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to evaluate apparent arbitrage opportunities such as price gaps, surebets, basis trades, multi-leg baskets, and cross-venue spreads. It helps produce fee-aware decision memos that classify lock quality, surface settlement and fill risks, and identify proceed, verify, watchlist, or reject next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitrage analysis may be mistaken for personalized financial, legal, or tax advice.

Mitigation: Frame outputs as market-structure analysis, avoid suitability recommendations, and include concise reminders that outcomes still depend on fills, fees, and settlement working as modeled.

Risk: Headline spreads can overstate edge when fees, financing, transfer costs, FX, depth, or settlement timing are incomplete.

Mitigation: Use fee-aware calculations, classify lock quality, identify missing cost lines, and reject or downgrade opportunities that do not survive net-edge and settlement checks.

Risk: Local notes in ~/arbitrage/ can persist user preferences, constraints, venue notes, and active opportunity details.

Mitigation: Use a narrow activation preference when desired, save only explicit user-stated constraints, and avoid providing exchange keys, wallet secrets, or broker credentials.

Risk: Live market data can be stale or unavailable unless the user provides it or explicitly asks for it to be fetched.

Mitigation: Reference timestamps and missing inputs, ask for current venue data when needed, and avoid calling an opportunity locked until the relevant quotes, rules, depth, and settlement mechanics are verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/arbitrage)
- [Skill Homepage](https://clawic.com/skills/arbitrage)
- [Locked Spread Protocol](artifact/workflow.md)
- [Fee-Aware Arbitrage Calculator](artifact/calculator.md)
- [Venue and Settlement Checks](artifact/venue-checks.md)
- [Arbitrage Playbooks](artifact/playbooks.md)
- [Safe Language for Arbitrage Analysis](artifact/legal.md)
- [Memory Template](artifact/memory-template.md)
- [Setup Guide](artifact/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown decision memos with plain-text formulas and occasional shell commands for local setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local notes under ~/arbitrage/; no credentials or extra binaries are required; live public data is used only when provided by the user or explicitly requested.]

## Skill Version(s):

1.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
