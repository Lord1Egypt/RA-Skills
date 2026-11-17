## Description:

Explains cryptocurrency price moves by matching volatility to recent events, market data, and on-chain context, while routing broader analysis requests to the appropriate Gate skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to understand why a cryptocurrency pumped or dumped by receiving a structured event attribution report with market and on-chain context. It is intended for explanation only, not trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package instructs agents to follow shared parent-directory runtime-rule files that are not included in the artifact.

Mitigation: Bundle, pin, or verify the referenced shared runtime rules before installation and review their contents before allowing the skill to run.

Risk: Event attribution can overstate causality when market, news, or on-chain evidence is incomplete.

Mitigation: Use cautious language, disclose missing data, preserve source attribution, and avoid buy, sell, or directional trading recommendations.

## Reference(s):

- [Gate News EventExplain MCP Specification](references/mcp.md)
- [Scenarios & Prompt Examples](references/scenarios.md)
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-news-event-explain)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown attribution report with tables and source-aware narrative sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include volatility summary, triggering event, impact chain, on-chain verification, ripple effects, forward outlook, uncertainty notes, and no-investment-advice disclaimers.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; artifact frontmatter version 2026.4.3-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
