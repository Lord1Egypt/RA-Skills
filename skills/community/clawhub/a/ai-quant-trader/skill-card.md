## Description: <br>
Ai Quant Trader is a simulated A-share stock analysis and quant-trading assistant that supports strategy generation, stock screening, paper trading, risk rules, and portfolio status commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuhuijiang2025-cell](https://clawhub.ai/user/yuhuijiang2025-cell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill through OpenClaw commands or conversation to explore A-share screening criteria, generate illustrative strategies, run simulated trades, and review stop-loss or take-profit rules before making any independent investment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Strategy recommendations, backtests, win rates, and some screening metrics may be mock, random, delayed, or illustrative. <br>
Mitigation: Treat every recommendation and metric as non-authoritative; independently verify market data, assumptions, and strategy performance before using them for real investing. <br>
Risk: The artifact includes setup and runtime code that can install dependencies, call AKShare data sources, and write local user-data, cache, strategy, position, and risk-rule files. <br>
Mitigation: Review setup scripts and runtime file-writing behavior before installation or deployment, and run the skill in an isolated environment when evaluating it. <br>
Risk: The skill exposes automatic-trading and risk-rule flows even though the release evidence characterizes trading behavior as simulated. <br>
Mitigation: Keep broker integrations in simulation mode unless a qualified reviewer confirms the code path, authorization model, and operational controls are appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuhuijiang2025-cell/ai-quant-trader) <br>
- [Publisher profile](https://clawhub.ai/user/yuhuijiang2025-cell) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Chinese natural-language responses, command-style prompts, Python code paths, and JSON configuration or strategy files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include simulated prices, strategy performance, screening metrics, trade records, and risk-rule settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
