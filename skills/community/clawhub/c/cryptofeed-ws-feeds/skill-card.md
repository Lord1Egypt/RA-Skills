## Description: <br>
实时获取多个加密货币交易所的市场数据流，支持异步回调处理并将交易、行情、订单簿等数据持久化到ArcticDB时序数据库。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative engineers use this skill to generate guidance, code, and commands for cryptocurrency exchange market-data feeds, async callbacks, order-book handling, time-series persistence, and related strategy or backtesting workflows. The artifact also includes broader finance and trading workflows that should be reviewed before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner found the skill suspicious because it combines crypto market-data ingestion with broader stock, backtesting, credentialed exchange, live-trading, external storage, and rate-limit-bypass guidance. <br>
Mitigation: Install it only when a broad finance or trading assistant is intended, and review generated workflows before execution. <br>
Risk: The skill may ask for sensitive exchange, broker, or provider credentials and can produce trading-related actions. <br>
Mitigation: Use read-only or paper-trading credentials by default and require explicit approval before live trading or credentialed account operations. <br>
Risk: Generated workflows may write market data or account-related data to external databases or storage sinks. <br>
Mitigation: Set clear storage locations, retention rules, and allowed external sinks before running generated commands or code. <br>
Risk: Rate-limit-bypass workflows can violate exchange terms or trigger API restrictions. <br>
Mitigation: Avoid rate-limit-bypass patterns unless they have been reviewed against the relevant exchange terms and operating limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/cryptofeed-ws-feeds) <br>
- [Publisher profile](https://clawhub.ai/user/tangweigang-jpg) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Human Summary](human_summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request market, provider, strategy, time range, entity IDs, credentials, and storage targets before producing executable guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata; artifact metadata version v6.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
