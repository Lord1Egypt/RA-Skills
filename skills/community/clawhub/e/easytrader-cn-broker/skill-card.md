## Description: <br>
Provides A-share broker client automation for XueQiu, YunHui, and related workflows, including login, account queries, order submission, position management, and portfolio following. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quant engineers use this skill to build broker-connected A-share trading workflows, expose broker operations through an API, validate account preparation, query balances and entrusts, cancel orders, and mirror portfolios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports real broker automation, including order submission, entrust cancellation, and portfolio following. <br>
Mitigation: Install only when broker-connected automation is intended; start in an isolated Python environment, validate dry-run behavior first, and require explicit confirmation for every live order or cancellation. <br>
Risk: The release mixes live trading workflows with quant research and backtesting flows, which can blur simulated and live execution paths. <br>
Mitigation: Keep research, backtesting, and live broker credentials in separate environments, label generated workflows as dry-run or live, and review generated server, heartbeat, or skill-file changes before running them. <br>
Risk: A-share trading workflows can be invalid or unsafe if execution constraints such as T+1 settlement, sell-before-buy ordering, and next-bar execution are not preserved. <br>
Mitigation: Check generated trading logic against the supplied semantic locks and domain constraints before using it for broker-connected activity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/easytrader-cn-broker) <br>
- [Human Summary](human_summary.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Domain Constraints](references/CONSTRAINTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose broker-connected actions; live orders and cancellations should require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.3.3 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
