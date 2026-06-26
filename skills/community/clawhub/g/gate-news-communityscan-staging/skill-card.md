## Description: <br>
Community sentiment via Gate-News MCP, X/Twitter-first, for social discussion, KOL takes, or opinion on a coin or topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to summarize crypto community sentiment from Gate-News X/Twitter discussion data and social sentiment metrics. It helps compare dominant narratives, KOL themes, sentiment scores, and price-sentiment alignment without presenting sentiment as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto social sentiment can be mistaken for financial advice or a reliable price predictor. <br>
Mitigation: Label outputs as informational community sentiment, include the skill's investment-advice disclaimer, and present bullish and bearish views neutrally. <br>
Risk: Coverage is X/Twitter-first and may omit Reddit, Discord, Telegram, or broader news context. <br>
Mitigation: State platform coverage clearly, label reports as X/Twitter-only when UGC search is unavailable, and route news or coin-analysis requests to the matching Gate skill. <br>
Risk: Unavailable Gate-News MCP tools can lead to partial or missing analysis. <br>
Mitigation: Use the documented graceful degradation path: continue with the available dimension, label missing data, or return a concise retry/setup message if all required tools fail. <br>
Risk: Rumors or KOL discussion may be unverified. <br>
Mitigation: Do not fabricate opinions or quotes, attribute only what the returned data supports, and describe rumors as unverified claims. <br>


## Reference(s): <br>
- [Gate News Community Scan Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gaixianggeng/gate-news-communityscan-staging) <br>
- [Third-Party Publisher Profile](https://clawhub.ai/user/gaixianggeng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown report with sentiment tables, narrative summaries, key takeaways, and limitations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Gate-News MCP outputs are synthesized into an X/Twitter-focused community sentiment report.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; skill frontmatter version: 2026.4.7-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
