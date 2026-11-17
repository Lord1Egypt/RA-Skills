## Description:

Generates a daily China A-share market review HTML report from Tongdaxin MCP and Tonghuashun iWencai data, covering limit-up reviews, theme grouping, consecutive-board tiers, capital flows, and related market modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinfa77-svg](https://clawhub.ai/user/jinfa77-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market analysts use this skill to collect A-share market data, assemble a structured report_data.json file, and generate a daily HTML market review report. The workflow is intended for market reporting and review, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External market data is transformed into local HTML, and the security summary notes that output escaping needs review.

Mitigation: Treat generated HTML as untrusted until escaping is verified or fixed, and open or share reports only in trusted environments.

Risk: The generated report includes actionable stock-trading sections.

Mitigation: Review trading-related sections as general market commentary and do not treat them as personalized financial advice.

Risk: The security guidance recommends use only with trusted working directories and trusted market-data sources.

Mitigation: Install and run the skill only in a trusted workspace with approved Tongdaxin MCP and Tonghuashun iWencai data sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinfa77-svg/skills/a-share-daily-report-publish)
- [Publisher profile](https://clawhub.ai/user/jinfa77-svg)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON structure, shell commands, and a generated HTML report file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires trusted Tongdaxin MCP and Tonghuashun iWencai market-data sources, then writes report_data.json and a dated HTML report.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
