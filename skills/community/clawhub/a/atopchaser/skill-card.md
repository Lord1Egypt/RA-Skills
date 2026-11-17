## Description:

Gets the current A-share top 10 gainers and provides buy, observe, or avoid commentary based on the returned market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ikaroso](https://clawhub.ai/user/ikaroso)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch a same-day A-share top-gainers table and turn it into concise short-term stock commentary with explicit non-advice disclaimers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's buy, hold, or avoid commentary could be mistaken for personalized financial advice.

Mitigation: Keep the non-investment-advice disclaimers in generated responses and require users to make their own investment decisions.

Risk: The helper script launches a headless browser and contacts a third-party Chinese market-data site.

Mitigation: Run the skill only in environments where outbound web access to the data source is acceptable and browser execution is permitted.

Risk: Same-day top-gainer rankings can be volatile or inaccurate if the source page changes, loads slowly, or returns incomplete data.

Mitigation: Review the raw script output before relying on the analysis and treat the commentary as time-sensitive market context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ikaroso/skills/atopchaser)
- [Publisher profile](https://clawhub.ai/user/ikaroso)
- [10jqka A-share gainers data source](https://data.10jqka.com.cn/market/zdfph/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with a code block containing raw script output, followed by per-stock commentary and a risk summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the fetched Top 10 table, buy/observe/avoid judgments, a market-sentiment summary, and non-investment-advice disclaimers.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
