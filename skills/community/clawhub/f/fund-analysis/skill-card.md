## Description:

Analyze mutual fund performance, holdings, risk metrics, and investment suitability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare mutual fund and public-market analysis, including fund rankings, holdings changes, risk metrics, macro indicators, and investment-suitability summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python dependencies for market-data access may affect the host environment if installed globally or with elevated privileges.

Mitigation: Install dependencies in an isolated virtual environment and avoid elevated-privilege package installation.

Risk: Generated fund and market analysis may be incomplete, stale, or unsuitable as investment advice.

Mitigation: Treat outputs as informational, verify important figures against authoritative sources, and apply human financial review before decisions.

Risk: The artifact documents fund_daily_report.py, but the inspected package does not ship that script.

Mitigation: Confirm required runtime files are present before relying on documented execution commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/fund-analysis)
- [Publisher profile](https://clawhub.ai/user/paudyyin)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with financial-analysis summaries, tables, Python snippets, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on public-market data availability, trading calendars, and third-party data-source responses.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
