## Description:

Trades a market when your estimated probability diverges from the live market price, with dry-run by default, context checks, reasoning tags, and optional live execution through AION.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssj124](https://clawhub.ai/user/ssj124)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill when an agent already has a probability estimate for a specific prediction market and needs a disciplined wrapper for checking live market context, calculating edge, and optionally executing an AION trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform sensitive live-trading actions and may involve wallet approvals or credential custody.

Mitigation: Keep dry-run mode enabled by default, require explicit confirmation before live trading or wallet-affecting actions, and use only test funds or a tightly limited account.

Risk: Trading SDK dependencies are not pinned to exact versions.

Mitigation: Pin and review dependency versions before using the skill with real credentials or funds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssj124/skills/aionmarket-sdk-divergence-trader)
- [Polymarket CLOB API endpoint](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Text]

**Output Format:** [Markdown guidance with bash and Python examples; the script prints text summaries and JSON trade results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AION API credentials and market inputs; live execution occurs only when the --live flag is used.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
