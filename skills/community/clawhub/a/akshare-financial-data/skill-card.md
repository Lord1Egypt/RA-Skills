## Description: <br>
Helps agents retrieve Chinese A-share market data and draft AkShare or ZVT workflows for data collection, factor analysis, screening, and backtesting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quant analysts use this skill to query China market data and prepare AkShare or ZVT data collection, screening, factor, and backtest workflows for A-share strategies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill mixes read-only AkShare data lookup with ZVT strategy, backtesting, code-writing, credential, and trading-execution workflows. <br>
Mitigation: Use it in an isolated environment and require explicit confirmation before generated code, backtests, local data writes, or broker-connected actions. <br>
Risk: Provider or broker credentials may be involved for paid data sources or trading workflows. <br>
Mitigation: Keep credentials out of chat and load them only through approved local secret or configuration mechanisms. <br>
Risk: Financial data APIs and generated strategies can produce misleading results if rate limits, calendar rules, T+1 settlement, or look-ahead controls are ignored. <br>
Mitigation: Review generated code against the documented semantic locks, preconditions, and domain constraints before relying on analysis or executing trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/akshare-financial-data) <br>
- [Publisher profile](https://clawhub.ai/user/tangweigang-jpg) <br>
- [Human summary](artifact/human_summary.md) <br>
- [Semantic locks and preconditions](artifact/references/LOCKS.md) <br>
- [Domain constraints](artifact/references/CONSTRAINTS.md) <br>
- [Component capability map](artifact/references/COMPONENTS.md) <br>
- [Known use cases](artifact/references/USE_CASES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated Python or ZVT examples and package installation commands; execution should be explicitly confirmed by the user.] <br>

## Skill Version(s): <br>
0.3.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
