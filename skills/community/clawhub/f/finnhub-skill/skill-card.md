## Description: <br>
Read-only market data skill for Finnhub that helps an agent retrieve stock, forex, crypto, company profile, candles/K-lines, news, earnings, and economic calendar data from Finnhub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samlin425](https://clawhub.ai/user/samlin425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch Finnhub market data, summarize quotes, profiles, news, earnings, economic calendar entries, and produce structured daily stock reports without placing trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Finnhub API key is required for live requests and could be exposed if routed through an untrusted host. <br>
Mitigation: Use a dedicated Finnhub key where possible and keep FINNHUB_BASE_URL on the official Finnhub domain. <br>
Risk: Some Finnhub endpoints may be unavailable because of API plan limits or quota usage. <br>
Mitigation: Report auth, quota, or plan-limit failures clearly and avoid fabricating fallback market data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samlin425/finnhub-skill) <br>
- [Finnhub API Reference Notes](references/api.md) <br>
- [Daily Stock News Report Template](references/daily-report-template.md) <br>
- [Finnhub API Base URL](https://finnhub.io/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Human-readable text or Markdown summaries, with optional JSON output when --raw is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Finnhub API retrieval using FINNHUB_API_KEY; broad requests should be narrowed before live calls.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
