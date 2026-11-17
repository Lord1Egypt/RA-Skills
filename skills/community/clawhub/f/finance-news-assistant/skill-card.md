## Description:

Monitors configured A-share and Hong Kong stock news, fetches market and AI decision data, and generates daily finance reports with source and anti-hallucination rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gushenjie](https://clawhub.ai/user/gushenjie)

### License/Terms of Use:

MIT-0

## Use Case:

External users who track the configured A-share and Hong Kong securities use this skill to generate daily market briefings, search recent stock news, and analyze likely news impact with explicit source and uncertainty handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the configured STOCK_API_TOKEN, queried stock symbols, request timing, and generated report data to a fixed external service.

Mitigation: Install only if the operator of tczlld.com is trusted, use a dedicated least-privilege token, and avoid including sensitive portfolio information in requests.

Risk: The skill can produce automated AI trading recommendations that may be incorrect or mistaken for professional financial advice.

Mitigation: Treat recommendations as unverified decision support, require human review before trading decisions, and preserve source citations and uncertainty labels.

Risk: Optional Feishu delivery may send generated reports to the configured recipient.

Mitigation: Enable Feishu delivery only after confirming the recipient ID and the operator's data-sharing requirements.

## Reference(s):

- [Finance News Assistant ClawHub Page](https://clawhub.ai/gushenjie/skills/finance-news-assistant)
- [Anti-Hallucination Rules](references/anti-hallucination.md)
- [Daily Report Format](references/daily-report-format.md)
- [News Source Allowlist](references/news-sources.md)
- [Known Error Log](references/error-log.md)
- [Configuration Example](assets/config.example.json)
- [Configured Stock API Base URL](https://tczlld.com/trade/api/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown finance reports and concise text responses with sourced news, API data, and analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily reports cover four A-share tickers and one Hong Kong ticker; each stock section is capped at 400 Chinese characters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
