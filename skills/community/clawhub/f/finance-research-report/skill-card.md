## Description:

A-share weekly finance research report generator that uses AKShare, Sina Finance, and Eastmoney data to produce technical analysis, trading signals, risk assessments, charts, and professional PDF reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mli-cj](https://clawhub.ai/user/mli-cj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this OpenClaw skill to generate local A-share weekly research reports for selected stock codes, including market overview, technical indicators, signal summaries, risk scoring, and position-sizing guidance. The generated analysis is informational and does not constitute investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can overwrite arbitrary writable files when a custom output path is supplied.

Mitigation: Run as an unprivileged user and avoid passing --output paths outside a dedicated report directory.

Risk: User-supplied author text and fetched market or news data are rendered into PDF content without escaping.

Mitigation: Keep user inputs plain text, review generated reports before sharing, and use trusted data/network environments.

Risk: The skill performs network-based finance-data retrieval and local PDF generation with third-party Python dependencies.

Mitigation: Use a virtual environment, pin and audit dependencies, and install only where network access to public finance sources is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mli-cj/skills/finance-research-report)
- [Publisher profile](https://clawhub.ai/user/mli-cj)
- [Sina Finance](https://finance.sina.com.cn/)
- [Sina quote API endpoint pattern](https://hq.sinajs.cn/list={sina_sym})

## Skill Output:

**Output Type(s):** [analysis, markdown, files, shell commands, guidance]

**Output Format:** [PDF report generated from HTML with charts; sample artifact also includes Markdown report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are saved locally under output/ by default, with optional custom output path support.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
