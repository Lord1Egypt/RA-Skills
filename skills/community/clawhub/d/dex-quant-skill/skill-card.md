## Description: <br>
Dex Skill helps agents create cryptocurrency trading strategy scripts from natural-language rules, run server-side backtests, optimize parameters, and set up strategy monitoring or execution for Binance and Hyperliquid markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miyaosk](https://clawhub.ai/user/miyaosk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate Python-based crypto trading strategies, backtest them, tune parameters, and monitor or execute strategies through supported exchange workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle wallet credentials and automate live crypto trades. <br>
Mitigation: Prefer signal-only, dry-run, or testnet mode first; use a dedicated low-balance wallet and never paste private keys into chat. <br>
Risk: The skill uploads strategy code to a server for backtesting or execution. <br>
Mitigation: Review strategy source before upload and verify the configured server URL before running backtests or enabling monitoring. <br>
Risk: Trading guidance, backtest results, or optimized parameters may be misleading or unsuitable for live markets. <br>
Mitigation: Treat outputs as decision support, review risk settings manually, and confirm behavior before using real funds. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/miyaosk/dex-quant-skill) <br>
- [Publisher profile](https://clawhub.ai/user/miyaosk) <br>
- [DEX Quant server endpoint](https://quant.supersafeclaw.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses, Python strategy files, shell command invocations, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce strategy source files, backtest or optimization summaries, chart attachments, and monitoring setup guidance.] <br>

## Skill Version(s): <br>
3.47.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
