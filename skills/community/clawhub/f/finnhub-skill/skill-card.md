## Description:

Read-only market data skill for Finnhub. Use when the user wants stock, forex, crypto, company profile, candles/K-lines, news, earnings, or economic calendar data from Finnhub; also use when the user mentions Finnhub API, Finnhub token, or wants to package Finnhub market data access into an OpenClaw workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samlin425](https://clawhub.ai/user/samlin425)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve read-only Finnhub market data for quotes, candles, company profiles, news, earnings, economic calendar data, and concise daily stock reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent needs access to a Finnhub API key for live market-data requests.

Mitigation: Install only when that access is acceptable, keep the key in the environment, restrict requests to the official Finnhub HTTPS domain, and avoid printing tokens in logs or errors.

Risk: Finnhub plan limits or auth errors can leave candles, volume, or other endpoints unavailable.

Mitigation: State auth, quota, or plan-limit failures clearly, use available quote and news data where appropriate, and do not fabricate missing market data.

Risk: Broad activation wording or the Chinese daily-report template may not match every workflow's routing or language expectations.

Mitigation: Review activation wording and report template language before deployment where routing precision or output language matters.

## Reference(s):

- [Finnhub API Reference Notes](references/api.md)
- [Daily Stock News Report Template](references/daily-report-template.md)
- [Finnhub API base URL](https://finnhub.io/api/v1)
- [ClawHub skill page](https://clawhub.ai/samlin425/skills/finnhub-skill)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Human-readable text or Markdown summaries, with optional raw JSON from Finnhub API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINNHUB_API_KEY for live requests; requests are read-only and restricted to the official Finnhub HTTPS domain.]

## Skill Version(s):

0.2.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
