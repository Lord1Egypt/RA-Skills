## Description:

Finance Data Fetcher helps agents retrieve Chinese A-share quotes, historical market data, financial reports, capital flows, and fundamental indicators through AkShare.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gbabyzs](https://clawhub.ai/user/gbabyzs)

### License/Terms of Use:

MIT-0

## Use Case:

Data-focused agents and financial analysis workflows use this skill to fetch Chinese A-share market, financial, capital-flow, and fundamental data for research, screening, and reporting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release metadata references a missing skill_main.py implementation file.

Mitigation: Verify that the publisher or package system supplies the implementation before installation or use.

Risk: Stock-code lookups may be external requests that can be logged by market data providers.

Mitigation: Treat requested symbols and usage patterns as potentially observable by upstream data providers.

Risk: The skill depends on external Python packages for market data access.

Mitigation: Pin and review dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gbabyzs/skills/finance-data-fetcher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and code-oriented guidance with Python function examples and dependency commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for calls that may depend on external market data availability, provider delays, and provider rate limits.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
