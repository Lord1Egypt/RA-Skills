## Description: <br>
Provides Finloop financial news search, market-period briefings, AI hot-news lookup, and stock quote retrieval through documented HTTP API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CZZLEGEND](https://clawhub.ai/user/CZZLEGEND) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Finloop finance news, AI hot-news details, market-period summaries, and real-time stock or index quote data when answering time-sensitive financial information requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some Finloop requests may require an sl-session cookie without clear consent, scoping, or credential-handling safeguards. <br>
Mitigation: Do not provide or reuse an sl-session cookie unless the user understands which account it belongs to and why the request needs it; prefer scoped or temporary credentials when available. <br>
Risk: Finance queries, tickers, and related request data are sent to Finloop endpoints. <br>
Mitigation: Install and use the skill only when the user trusts the Finloop package and is comfortable sharing those queries with the listed Finloop services. <br>
Risk: Returned market data, rankings, and news summaries may be incomplete, delayed, or unsuitable as the sole basis for financial decisions. <br>
Mitigation: Treat results as informational and verify important financial decisions against additional authoritative sources. <br>


## Reference(s): <br>
- [Finloop News API Reference](.agents/skills/finloop-news-skill/references/REFERENCE.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/CZZLEGEND/finloop-news-skills) <br>
- [Finloop News API Base](https://ai-uat.finloopfintech.com) <br>
- [Finloop Market Data API Base](https://papi-uat.finloopg.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON-derived text responses with direct HTTP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include categorized finance-news summaries, AI hot-news details, market-period briefs, stock quote fields, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
