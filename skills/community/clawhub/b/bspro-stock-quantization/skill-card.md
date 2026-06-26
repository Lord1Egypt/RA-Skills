## Description: <br>
BSpro Stock Quantization helps agents query and analyze A-share market data, screen stocks, compute common quantitative indicators, run backtests, assess stock risk, and generate MOE factor-based buy and sell signal reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eventaumjohn](https://clawhub.ai/user/eventaumjohn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to answer Chinese A-share stock research questions, fetch market and fundamentals data, calculate technical and quantitative indicators, run strategy backtests, and present structured investment-analysis reports. It is intended to support analysis workflows, not to replace professional financial judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads, decrypts, unzips, and imports market-data updates from the publisher backend into a local database. <br>
Mitigation: Install only if the publisher backend is trusted, review update behavior before use, and run the skill in an isolated environment when handling sensitive work. <br>
Risk: The skill uses BITSOUL_TOKEN for remote data access and may read it from an explicitly configured env file. <br>
Mitigation: Use a token dedicated to this service, keep it out of shared logs and prompts, and restrict BITSOUL_TOKEN_ENV_FILE to a file that contains only the intended token. <br>
Risk: Optional performance or positions submission can upload strategy results to a remote service. <br>
Mitigation: Invoke submission or leaderboard-related APIs only when remote sharing is intended, and review submitted fields before sending. <br>
Risk: Generated trading analysis and buy or sell signals can be incomplete, stale, or misleading. <br>
Mitigation: Treat outputs as analytical support, verify results against independent market data, and include financial-risk disclaimers in user-facing reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eventaumjohn/bspro-stock-quantization) <br>
- [Publisher profile](https://clawhub.ai/user/eventaumjohn) <br>
- [AICodingYard homepage](https://www.aicodingyard.com) <br>
- [API_FOR_LLM.md](references/API_FOR_LLM.md) <br>
- [Sina Finance](https://finance.sina.com.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance] <br>
**Output Format:** [Simplified Chinese markdown reports with tables, structured JSON from API calls, and occasional shell configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include stock codes with names, model scores, backtest summaries, risk notes, and supporting market data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
