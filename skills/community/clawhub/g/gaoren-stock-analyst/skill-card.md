## Description:

Generates comprehensive stock analysis reports for HK, US, and A-share symbols using market data, technical indicators, financial metrics, and multi-source news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate stock analysis reports for HK, US, and A-share tickers, including quotes, technical indicators, financial ratios, news sentiment, and a synthesized judgment. The reports support market research workflows and require human review before investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill embeds a Finnhub API token in source files.

Mitigation: Rotate and remove the hardcoded token, then require user-supplied credentials through a secure environment variable before use.

Risk: Generated reports can present simulated technical indicators and investment-style recommendations as reliable guidance.

Mitigation: Use real historical market data for indicators or clearly label simulated values, and require human review before any trading decision.

Risk: Stock symbols are sent to external market and news providers.

Mitigation: Inform users before use and avoid submitting sensitive, private, or non-public watchlists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaoren36-arch/skills/gaoren-stock-analyst)
- [README.md](artifact/README.md)
- [README_EN.md](artifact/README_EN.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain-text stock analysis report with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include real-time quotes, technical indicators, news sentiment, valuation scoring, and investment-style recommendations; external provider availability and credentials affect completeness.]

## Skill Version(s):

3.0.0 (source: server release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
