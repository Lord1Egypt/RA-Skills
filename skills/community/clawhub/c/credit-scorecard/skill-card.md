## Description: <br>
基于监督学习、决策树或聚类等多种算法，自动为评分卡变量生成最优分箱边界，同时支持单调性约束和缺失值处理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and credit-risk practitioners use this skill to design scorecard workflows, including feature bucketing, Weight of Evidence encoding, feature selection, logistic-regression scorecard training, scaling, validation, and deployment guidance. Reviewers should note that the release evidence also flags substantial stock, crypto, market-data, and backtesting content outside the advertised scorecard scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is advertised as credit-scorecard bucketing but includes stock and crypto trading, market-data, backtesting, and local setup workflows. <br>
Mitigation: Review generated guidance for scope drift before use, and install only when both scorecard and ZVT quant/backtesting assistance are intended. <br>
Risk: Generated workflows may fetch data, require provider or broker login, or produce order-related trading steps. <br>
Mitigation: Require explicit user confirmation before any data fetch, provider login, broker login, or order-related workflow, and avoid providing paid-provider or broker credentials unless generated code and data paths are clear. <br>
Risk: Local setup guidance may introduce Python package and environment risk. <br>
Mitigation: Use an isolated Python environment and pin and review dependencies before installing zvt or related packages. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tangweigang-jpg/credit-scorecard) <br>
- [Human Summary](human_summary.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Constraints](references/CONSTRAINTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for market, data provider, strategy type, time range, and entity identifiers before generating workflow-specific guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
