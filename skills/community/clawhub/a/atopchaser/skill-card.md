## Description: <br>
获取当前 A 股涨幅 Top10 并基于结果给出是否值得买入的分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ikaroso](https://clawhub.ai/user/ikaroso) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to fetch the current A-share gainers Top 10, reproduce the script output, and receive concise stock-by-stock buy/watch/avoid commentary. The analysis is informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local script opens a headless browser and fetches public stock data from a third-party market-data site. <br>
Mitigation: Run it in an environment where Playwright and Python dependencies come from trusted sources, and review network access before use. <br>
Risk: Stock buy/watch/avoid commentary may be incomplete, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Treat the output as informational analysis only, include the non-investment-advice warning, and require users to make their own investment decisions. <br>


## Reference(s): <br>
- [ATopChaser on ClawHub](https://clawhub.ai/ikaroso/atopchaser) <br>
- [Publisher profile: ikaroso](https://clawhub.ai/user/ikaroso) <br>
- [10jqka A-share gainers page](https://data.10jqka.com.cn/market/zdfph/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with a verbatim script-output code block and concise stock-by-stock analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a non-advice risk note and depends on current public market data returned by the local script.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
