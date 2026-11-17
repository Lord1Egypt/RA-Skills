## Description:

Provides China A-share market quotes, individual stock analysis, market sentiment, sector highlights, trading strategy suggestions, and price alert support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer China A-share stock questions, summarize market data, analyze individual stocks and sectors, and draft risk-labeled trading strategy suggestions.

### Deployment Geography for Use:

Global; the skill content is focused on mainland China A-share markets.

## Known Risks and Mitigations:

Risk: Generated buy, sell, stop-loss, take-profit, or position-size suggestions could be mistaken for professional financial advice.

Mitigation: Treat outputs as decision support only, keep explicit risk notices, and require users to verify recommendations with independent market data or qualified financial advice.

Risk: Real-time market data may be stale, unavailable, or inconsistent across public data sources.

Mitigation: Show the data source and retrieval time, and ask users to cross-check material trading decisions against a broker or authoritative market data feed.

Risk: The inspected artifact references helper scripts and watchlist files that were not present in the artifact.

Mitigation: Confirm the expected files and tools exist before relying on automation, and fall back to manual data verification when they are unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvis-a-stock-trading-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with tables, bullet points, risk notes, and occasional bash command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market data responses should include source and retrieval time; trading suggestions should include risk caveats.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
