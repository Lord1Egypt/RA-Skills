## Description: <br>
Models asset-backed securities deal structures, mortgage-pool cash flows, tranche repayment, and waterfall allocations, while the packaged artifact also includes quant trading and backtesting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance analysts use this skill to draft ABS cash-flow models, waterfall logic, tranche analysis, and related reports. Reviewers should also expect stock and crypto quant backtesting guidance because the artifact contains ZVT trading workflows in addition to ABS examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled as ABS cash-flow modeling, but the artifact also directs agents into stock and crypto quant backtesting, broker or provider setup, and persistent skill-file creation. <br>
Mitigation: Review the generated plan before execution, restrict use to an isolated offline or backtest environment unless market-data and trading workflows are intended, and disable unwanted persistent skill-file creation. <br>
Risk: Trading or market-data workflows can involve broker or paid-provider credentials. <br>
Mitigation: Do not provide broker or paid-provider credentials unless explicitly required and approved for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/abs-cashflow-modeling) <br>
- [Human summary](artifact/human_summary.md) <br>
- [Known use cases](artifact/references/USE_CASES.md) <br>
- [Semantic locks and preconditions](artifact/references/LOCKS.md) <br>
- [Component capability map](artifact/references/COMPONENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Python and ZVT workflows; generated financial or trading outputs require independent review before use.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
