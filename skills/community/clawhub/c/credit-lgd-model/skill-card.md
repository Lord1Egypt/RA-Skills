## Description: <br>
Provides guidance for building and training LGD credit-risk models, while the packaged artifacts also include ZVT quant-trading workflow material that should be reviewed before use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial analysts can use this skill as a ClawHub assistant for credit-risk and LGD modeling tasks. Review workflows carefully because the bundled artifacts emphasize ZVT data collection, backtesting, and trading-strategy code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled as an LGD credit-risk model, but the artifacts mainly guide ZVT quant trading and backtesting workflows. <br>
Mitigation: Review the skill before installation and use it only when that quant-trading/backtesting behavior is intended. <br>
Risk: Broker or paid data-provider credentials could be requested by workflows that are not explicit enough for the intended LGD use case. <br>
Mitigation: Use an isolated Python environment and do not provide credentials unless the exact workflow and provider interaction are separately approved. <br>
Risk: Trading outputs could be mistaken for live-trading recommendations or actions. <br>
Mitigation: Treat generated trading outputs as offline backtests unless live actions are separately reviewed and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/credit-lgd-model) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Human summary](artifact/human_summary.md) <br>
- [Component capability map](artifact/references/COMPONENTS.md) <br>
- [Known use cases](artifact/references/USE_CASES.md) <br>
- [Semantic locks and preconditions](artifact/references/LOCKS.md) <br>
- [Anti-patterns](artifact/references/ANTI_PATTERNS.md) <br>
- [Cross-project wisdom](artifact/references/WISDOM.md) <br>
- [Constraints](artifact/references/CONSTRAINTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local installs, data-provider setup, backtest code, and model workflow guidance for review before execution.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
