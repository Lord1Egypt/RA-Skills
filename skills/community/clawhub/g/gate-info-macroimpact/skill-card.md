## Description:

Macro-driven crypto via Gate-Info and Gate-News MCP. Use this skill whenever macro events such as CPI, NFP, Fed decisions, rates, or payrolls need to be connected to crypto market context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate macro-to-crypto impact reports from economic calendar, macro indicator, news, and market snapshot data. It is intended for read-only analysis of how macro events may relate to crypto market behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad macro trigger terms such as Fed or rates may capture generic questions that need stricter routing.

Mitigation: Confirm the user is asking for macro-to-crypto impact analysis and route pure market, technical, or news-only requests to the matching skill.

Risk: Missing Gate Info or Gate News MCP tools can make the report incomplete.

Mitigation: Check MCP availability before use, skip unavailable sections, label missing dimensions clearly, and stop with setup guidance if all required tools fail.

Risk: Macro and crypto correlations may be mistaken for deterministic forecasts or trading advice.

Mitigation: Use neutral, data-driven language, avoid buy or sell recommendations, avoid specific price predictions, and state that macro-crypto impacts are probabilistic.

## Reference(s):

- [Gate Info Macro Impact Runtime Rules](artifact/references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](artifact/references/info-news-runtime-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-info-macroimpact)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with tables and concise analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only Gate Info and Gate News MCP tool results when available; no local file writes or credential handling during normal execution.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter version: 2026.4.6-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
