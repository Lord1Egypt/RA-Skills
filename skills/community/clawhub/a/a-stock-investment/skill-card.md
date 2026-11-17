## Description:

Provides A-share market search and analysis for index trends, sector rotation, capital flows, and market hotspots using Tavily search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fmouseboy](https://clawhub.ai/user/fmouseboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather current A-share market information and draft concise market-analysis reports. It is intended for informational market research, not as a substitute for professional financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market search results or generated analysis may be stale, incomplete, or unsuitable as financial advice.

Mitigation: Treat outputs as informational and verify important claims against reliable financial sources before making decisions.

Risk: Market-search queries are sent to Tavily and could expose sensitive information if prompts include private data, account details, or trading plans.

Mitigation: Use only non-sensitive queries and keep private financial data or confidential trading plans out of prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fmouseboy/skills/a-stock-investment)
- [Tavily](https://tavily.com/)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown market-analysis report with answer and source sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY; search result count is capped by the script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
