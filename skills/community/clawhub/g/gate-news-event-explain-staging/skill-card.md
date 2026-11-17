## Description:

Explains crypto price moves by matching recent market volatility to Gate News events, market snapshots, and on-chain context, then producing an event attribution report with uncertainty noted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to understand why a cryptocurrency pumped, dumped, crashed, or surged by tracing likely triggering events, market reaction, and on-chain signals. It is intended for explanation and attribution only, not investment advice or trading decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad trigger phrases may cause the skill to activate for crypto requests that need a different analysis workflow.

Mitigation: Review trigger boundaries and route multi-dimension, general news, technical analysis, and market overview requests to the documented sibling skills.

Risk: Event attribution can overstate causality when market moves have multiple overlapping causes or incomplete data.

Mitigation: Use the skill's uncertainty language, preserve source attribution, disclose missing data, and avoid definitive causal claims or trading recommendations.

Risk: The workflow queries Gate MCP services for market, news, event, and on-chain data.

Mitigation: Install only in environments where this read-only data access is acceptable and verify Gate News and Gate Info MCP availability before use.

## Reference(s):

- [Gate News EventExplain MCP Specification](references/mcp.md)
- [Scenarios & Prompt Examples](references/scenarios.md)
- [ClawHub Skill Page](https://clawhub.ai/gaixianggeng/skills/gate-news-event-explain-staging)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with tables, causal-chain sections, source attribution, and uncertainty notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only workflow; uses Gate News and Gate Info MCP data when available and degrades by disclosing missing data.]

## Skill Version(s):

1.0.1 (source: server release metadata); artifact frontmatter version 2026.4.3-1

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
