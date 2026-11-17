## Description:

Helps agents answer China A-share stock questions using AkShare-style examples for real-time quotes, historical K-lines, financial data, technical indicators, and stock screening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-nova86](https://clawhub.ai/user/mr-nova86)

### License/Terms of Use:


## Use Case:

Developers, analysts, and external users use this skill to guide A-share quote lookup, K-line retrieval, financial data checks, and technical-screening workflows by stock code or stock name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send stock queries to external financial data services.

Mitigation: Use an isolated Python environment, pin dependencies where possible, and review data-provider terms before use.

Risk: Some documentation exceeds the stated A-share scope and real-time market data may be delayed.

Mitigation: Confirm the intended market coverage, validate important prices against trusted sources, and disclose latency when using outputs for analysis.

Risk: Bundled chart scripts write to a fixed chart filename.

Mitigation: Review and adjust output paths before execution so generated files are written only to intended locations.

## Reference(s):

- [ClawHub skill page: A Stock Data](https://clawhub.ai/mr-nova86/skills/a-stock-data)
- [ClawHub publisher profile: mr-nova86](https://clawhub.ai/user/mr-nova86)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock data field descriptions, AkShare query examples, technical analysis snippets, and chart-generation commands.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter declares 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
