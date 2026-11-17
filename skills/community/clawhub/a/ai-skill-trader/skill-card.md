## Description:

An aion-sdk powered Polymarket thesis trader that scans prediction markets for a configurable thesis, compares user probability to market price, and trades only when the edge clears a safety threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gulangduchuangtianyu](https://clawhub.ai/user/gulangduchuangtianyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan Polymarket markets for a configurable thesis, compare a supplied fair probability against market prices, and produce dry-run trade proposals or live trades when enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place repeated trades on a schedule without built-in exposure limits or duplicate-order safeguards.

Mitigation: Keep the skill in dry-run until position limits, duplicate-order protection, and daily spend caps are added.

Risk: A broad AION API key could allow unintended trading impact if live mode is enabled or misconfigured.

Mitigation: Use a restricted AION key with external account-level limits and enable live mode only after operator review.

Risk: Unpinned dependencies can change trading behavior over time.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gulangduchuangtianyu/skills/ai-skill-trader)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text operator summary with Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to dry-run; live trading requires --live or RUN_LIVE=true.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
