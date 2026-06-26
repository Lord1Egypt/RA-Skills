## Description: <br>
Community sentiment via Gate-News MCP, X/Twitter-first. Use for social discussion, KOL takes, or opinion on a coin or topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to summarize crypto community sentiment, X/Twitter discussion themes, KOL views, and social sentiment metrics for a coin or topic. It is intended for read-only community insight, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sentiment queries may be sent to the configured Gate-News MCP server. <br>
Mitigation: Install and use the skill only with a Gate-News MCP server you trust. <br>
Risk: Prompts could include private keys, account secrets, or sensitive personal details. <br>
Mitigation: Do not include secrets or sensitive personal information in sentiment-scan prompts. <br>
Risk: Community sentiment can be mistaken for financial advice or a price forecast. <br>
Mitigation: Present the output as community sentiment only and include the skill's investment-advice caveat. <br>


## Reference(s): <br>
- [Gate News Community Scan Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with sentiment summaries, metrics tables, takeaways, and caveats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [X/Twitter-only until broader UGC search is available; output should distinguish community sentiment from price prediction or investment advice.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
