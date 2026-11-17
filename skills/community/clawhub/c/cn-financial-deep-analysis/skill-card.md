## Description:

Generates A-share financial analysis, fraud-risk screening, sector analysis, valuation commentary, and structured research reports using a macro, statement-level, and transaction-level framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to screen and analyze A-share companies, compare industries, identify financial-statement risk signals, and draft structured investment research reports. Optional helpers can turn analysis results into PNG charts or Word documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require installing mutable third-party code and unpinned Python dependencies for its data-source and optional output helpers.

Mitigation: Install dependencies in an isolated virtual environment and pin or verify the exact Git commit and Python package versions before use.

Risk: Generated financial analysis and investment conclusions can be incomplete, stale, or misleading if source data is delayed or interpreted incorrectly.

Mitigation: Treat outputs as draft analysis and require review by a qualified financial professional before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/cn-financial-deep-analysis)
- [Three-layer analysis framework](references/core/three-layer-framework.md)
- [Fraud detection and warning signals](references/core/fraud-detection.md)
- [Financial scoring system](references/core/scoring-system.md)
- [Industry module index](references/industries/README.md)
- [Classic fraud case library](references/cases/README.md)
- [cn-financial-mcp data source](https://github.com/ccq1/cn-financial-mcp.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with optional JSON-driven PNG charts and Word documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Investment conclusions are draft analysis and should be reviewed by a qualified professional before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
