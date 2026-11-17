## Description:

Analyzes Chinese A-share corporate announcements, policy changes, M&A, buybacks, placements, unlocks, and other events to assess likely stock-price and fundamental impacts using market data and primary web sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzswk](https://clawhub.ai/user/yzswk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and financial-analysis agents use this skill to interpret A-share events such as announcements, policy changes, restructurings, buybacks, placements, lockup expirations, and incentive plans. It helps structure event classification, source gathering, quantitative and qualitative impact assessment, historical comparison, and formal or brief analysis output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial conclusions may be incorrect or stale if based on incomplete market data, secondary commentary, or outdated web sources.

Mitigation: Verify important conclusions against original company filings, official policy documents, and current market data before relying on the analysis.

Risk: Event impact can be overstated when short-term price reaction is treated as lasting fundamental change.

Mitigation: Separate short-term market reaction from long-term fundamental impact and document impact duration, certainty, and whether the event was already expected.

Risk: Historical event comparisons may be misleading when applied mechanically to a new company, policy, or market setting.

Mitigation: Use historical examples only as supporting context and preserve company-specific, industry-specific, and policy-specific differences in the final assessment.

## Reference(s):

- [Event analysis guide](references/event-analysis-guide.md)
- [ClawHub skill page](https://clawhub.ai/yzswk/skills/a-share-event)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown event analysis with optional tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports a formal institutional commentary style or a brief personal-note style.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
