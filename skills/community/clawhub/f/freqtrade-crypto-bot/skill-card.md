## Description: <br>
Uses the Freqtrade framework to load multi-exchange OHLCV history and analyze trading strategy backtests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-strategy researchers use this skill to draft or review market-data loading, strategy analysis, and backtesting workflows. Treat outputs as offline backtesting guidance unless a human explicitly authorizes installation, data fetching, broker connections, or order-related commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags the release as suspicious because Freqtrade crypto branding conflicts with ZVT and A-share instructions. <br>
Mitigation: Review the skill before installing and verify the intended market, framework, and data provider before relying on generated guidance. <br>
Risk: The skill covers high-impact trading surfaces, including data fetching, broker or exchange connectivity, wallet-related capability tags, and order-related workflows. <br>
Mitigation: Use an isolated environment, avoid real exchange, broker, wallet, JoinQuant, or QMT credentials, and require manual confirmation before installs, data fetches, broker connections, or order-related commands. <br>
Risk: Generated backtesting or strategy guidance can be misleading if it violates the artifact's timing, data-quality, or execution constraints. <br>
Mitigation: Treat generated outputs as review material and check them against the semantic locks and constraints before running code or acting on results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tangweigang-jpg/freqtrade-crypto-bot) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Human Summary](artifact/human_summary.md) <br>
- [Semantic Locks](artifact/references/LOCKS.md) <br>
- [Constraints](artifact/references/CONSTRAINTS.md) <br>
- [Anti-Patterns](artifact/references/ANTI_PATTERNS.md) <br>
- [Component Capability Map](artifact/references/COMPONENTS.md) <br>
- [Use Cases](artifact/references/USE_CASES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with optional code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may describe backtesting or trading workflows and should be reviewed before use with credentials, brokers, wallets, or live orders.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata; artifact metadata reports v6.1 compilation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
