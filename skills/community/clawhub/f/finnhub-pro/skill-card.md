## Description: <br>
Finnhub Pro helps agents run Finnhub-powered U.S. stock market data lookups for quotes, company profiles, news, analyst recommendations, insider transactions, earnings calendars, financial metrics, market status, peer companies, and ticker search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lsj210001](https://clawhub.ai/user/lsj210001) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, analysts, and agent operators use this skill to query Finnhub market data from a Python CLI for U.S. equity research and workflow support. It is intended for quick quote, profile, news, recommendation, insider, earnings, financial, market-status, peer, and symbol-search lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finnhub API key exposure through prompts, shell history, logs, or local configuration. <br>
Mitigation: Provide the key through FINNHUB_API_KEY, avoid sharing it in prompts or logs, and redact it from any captured command output. <br>
Risk: Finnhub free-tier limits or paid-only endpoints can return 429 or 403 errors and interrupt workflows. <br>
Mitigation: Use the documented free-tier commands, keep request volume within the stated limit, and review any dependency installation or paid-upgrade prompt before approving it. <br>
Risk: Market-data responses can be incomplete, delayed, or unsuitable as the sole basis for financial decisions. <br>
Mitigation: Treat outputs as reference data, verify important results against authoritative sources, and avoid using the skill as investment advice. <br>


## Reference(s): <br>
- [Finnhub](https://finnhub.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/lsj210001/finnhub-pro) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/lsj210001) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal text or JSON from Finnhub API lookups, with setup and command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINNHUB_API_KEY; free-tier rate limits and paid-endpoint restrictions may apply.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
