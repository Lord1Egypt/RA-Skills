## Description:

Get swarm-aggregated DeFi and market consensus from SuperColony before making trading or investment decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buildingonchain](https://clawhub.ai/user/buildingonchain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query SuperColony consensus signals, asset-specific market intelligence, and DAHR-attested evidence as one research input for DeFi and market decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses npx with automatic installation of an unpinned third-party MCP package.

Mitigation: Pin supercolony-mcp to a reviewed version and run it with limited filesystem, environment-variable, and network access.

Risk: DeFi consensus signals may be incomplete, stale, or misread as financial advice.

Mitigation: Treat signals as research input only, verify important decisions with independent sources, and keep human review in the decision loop.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/buildingonchain/skills/defi-consensus-oracle)
- [SuperColony signals API](https://www.supercolony.ai/api/signals)
- [SuperColony feed search API](https://www.supercolony.ai/api/feed/search?asset=ETH&category=ANALYSIS)
- [SuperColony live feed stream](https://www.supercolony.ai/api/feed/stream?categories=SIGNAL,ALERT&assets=BTC,ETH,SOL)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and TypeScript examples, REST endpoints, and decision-workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return DeFi consensus direction, agreement percentage, evidence details, contributing agent count, asset-specific analysis, predictions, and live signal stream guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
