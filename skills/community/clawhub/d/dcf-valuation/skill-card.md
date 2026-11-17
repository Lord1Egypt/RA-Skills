## Description:

This skill helps agents create ten-year valuation reports using traditional DCF and PE-exit methods, supported by qualitative business analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianzheng001](https://clawhub.ai/user/ianzheng001)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and finance-focused analysts use this skill to gather company inputs, assess qualitative business quality, run DCF and PE-exit scenarios, and draft a Markdown valuation report. Outputs are for reference and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial valuation reports can be misleading when source data is stale or assumptions are subjective.

Mitigation: Use the latest annual report and market data, document key assumptions, and treat the generated report as reference material rather than investment advice.

Risk: Optional Feishu sync can send investment notes or company analysis to a third-party cloud service.

Mitigation: Keep Feishu sync disabled for confidential notes unless the user explicitly accepts that cloud transfer.

Risk: Mutable install sources can differ from the version reviewed for release.

Mitigation: Install from a reviewed pinned version when possible.

## Reference(s):

- [DCF qualitative analysis framework](references/qualitative.md)
- [ClawHub skill page](https://clawhub.ai/ianzheng001/skills/dcf-valuation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown valuation report with calculation tables, qualitative analysis, and scenario judgments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local calculator prints traditional DCF and PE-exit scenario results and the skill may save Markdown reports to a user workspace path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
