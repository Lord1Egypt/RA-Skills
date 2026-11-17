## Description:

Build and test systematic daily-to-weekly trading algorithms through hypothesis, signal validation, backtesting, walk-forward validation, and paper-trading gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonbistudio](https://clawhub.ai/user/tonbistudio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, systematic traders, and research teams use this skill to structure trading-strategy research before live deployment. It guides users through hypothesis definition, isolated signal testing, strategy specification, in-sample backtesting, walk-forward validation, paper trading, and small-size live rollout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to create local research files and trading-analysis scripts.

Mitigation: Install it only in a workspace where that file creation is acceptable, and review generated code before running it.

Risk: Trading-analysis outputs may be incorrect or overfit and could inform real-capital decisions.

Mitigation: Review generated code, assumptions, and results before relying on them, especially before risking real capital.

## Reference(s):

- [Algo Builder on ClawHub](https://clawhub.ai/tonbistudio/skills/algo-builder)
- [Tonbi Studio](https://www.tonbistudio.com)
- [Active Portfolio Management](https://www.mheducation.com/highered/product/active-portfolio-management-quantitative-theory-applications-grinold-kahn/M9780070248823.html)
- [Advances in Financial Machine Learning](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086)
- [The Deflated Sharpe Ratio](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551)
- [Optimal Execution of Portfolio Transactions](https://www.smallake.kr/wp-content/uploads/2016/03/optliq.pdf)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python code templates, file paths, checklists, and command-oriented workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local algo-builder research files and trading-analysis scripts when the agent follows the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
