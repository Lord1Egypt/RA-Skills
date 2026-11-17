## Description:

Free stock analysis skill that pulls live data with yfinance and analyzes a single stock ticker for valuation metrics, financial health, and analyst consensus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apex-stack-ai](https://clawhub.ai/user/apex-stack-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request a single-ticker stock snapshot with market price, valuation ratios, financial-health indicators, and analyst consensus. It is suited for lightweight market research, not portfolio comparison or custom scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on yfinance and its transitive dependencies, which may change behavior or contain vulnerabilities if installed without version control.

Mitigation: Install in a virtual environment and pin yfinance and dependencies before use.

Risk: Public market data and analyst consensus can be delayed, incomplete, or unsuitable as the sole basis for financial decisions.

Mitigation: Verify important values against authoritative market-data sources and treat the output as informational analysis, not investment advice.

## Reference(s):

- [Financial Data Analyzer Lite on ClawHub](https://clawhub.ai/apex-stack-ai/skills/financial-analyzer-lite)
- [Apex Stack Publisher Profile](https://clawhub.ai/user/apex-stack-ai)
- [Financial Data Analyzer Full](https://apexstack.gumroad.com/l/financial-analyzer)
- [Apex Stack](https://apexstack.gumroad.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with optional inline shell commands for installing yfinance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-ticker analysis only; no comparison mode, custom scoring, or export functionality.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
