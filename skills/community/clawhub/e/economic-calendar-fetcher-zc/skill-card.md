## Description:

Fetch upcoming economic events and data releases using FMP API. Retrieve scheduled central bank decisions, employment reports, inflation data, GDP releases, and other market-moving economic indicators for specified date ranges (default: next 7 days). Output chronological markdown reports with impact assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and market-facing agents use this skill to retrieve scheduled economic data releases from FMP, filter them by date, country, event type, or impact level, and produce chronological market-calendar reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an FMP API key, which could be exposed if pasted into chat, command examples, or logs.

Mitigation: Provide the key through FMP_API_KEY or a secret manager, avoid echoing real keys in prompts or saved examples, and rotate any key that may have been exposed.

Risk: Reports can be saved to disk, so an unintended output path could disclose or overwrite local files.

Mitigation: Use an explicit, intended output path for saved reports and review the destination before execution.

Risk: Economic calendar data and impact labels may be incomplete, delayed, revised, or unsuitable as a sole basis for financial decisions.

Mitigation: Treat generated market implications as planning context, verify high-impact releases against authoritative sources, and avoid presenting the output as financial advice.

## Reference(s):

- [FMP Economic Calendar API Documentation](references/fmp_api_documentation.md)
- [FMP Economic Calendar API Endpoint](https://financialmodelingprep.com/api/v3/economic_calendar)
- [Financial Modeling Prep](https://financialmodelingprep.com)
- [ClawHub Skill Page](https://clawhub.ai/lean-zhouchao/skills/economic-calendar-fetcher-zc)
- [ClawHub Publisher Profile](https://clawhub.ai/user/lean-zhouchao)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with optional JSON or plain-text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write economic calendar output to stdout or to a user-specified file path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
