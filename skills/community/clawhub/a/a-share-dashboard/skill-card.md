## Description:

A Share Dashboard is a Streamlit web dashboard for A-share stock screening, hotspot tagging, individual stock analysis, northbound-capital tracking, and portfolio monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superhhh1992-byte](https://clawhub.ai/user/superhhh1992-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can run a local Streamlit dashboard to review A-share market conditions, stock fundamentals, K-line charts, portfolio positions, and risk alerts. The generated analysis is informational and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard executes a Python script from a separate local skill path that was not part of the reviewed package.

Mitigation: Install and use it only after verifying the separate a-share-stock-dossier skill and its script source.

Risk: Portfolio entries and market analysis may include sensitive financial details or misleading investment signals.

Mitigation: Avoid entering sensitive portfolio details unless you understand where the data is processed, and treat dashboard output as informational rather than investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superhhh1992-byte/skills/a-share-dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Streamlit dashboard with Markdown reports, Plotly charts, metrics, warnings, and launch commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Refreshes cached market data every five minutes and displays informational stock analysis only.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
