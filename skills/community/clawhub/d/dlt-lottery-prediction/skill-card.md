## Description:

DLT大乐透预测 v4.0 generates Chinese Sports Lottery DLT number recommendations using historical draw data, weighted number pools, strategy fusion, constraints, backtesting, and compound bet generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovensr](https://clawhub.ai/user/lovensr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to generate and inspect DLT lottery number recommendations, compound betting options, validation results, training workflows, and backtesting outputs. Treat the results as entertainment rather than financial guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may influence gambling spend through lottery predictions and betting recommendations.

Mitigation: Present predictions as entertainment only and avoid using them as financial advice or as a basis for high-stakes decisions.

Risk: The skill reads a local DLT Excel file and may fail or expose unintended local data if configured to an unexpected path.

Mitigation: Run it in a trusted workspace with an explicit, reviewed data file path and avoid sharing sensitive local files with the skill.

Risk: The skill may load local Python model artifacts with unsafe loading patterns.

Mitigation: Use only trusted model artifacts and review or isolate the workspace before enabling model loading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovensr/skills/dlt-lottery-prediction)
- [Artifact skill documentation](artifact/SKILL.md)
- [Strategy fusion design report](artifact/STRATEGY_FUSION_DESIGN.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured Python dictionaries containing predicted number sets, compound bet options, scores, validation results, and backtest summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read a local DLT Excel file and load or write local model artifacts depending on the workflow invoked.]

## Skill Version(s):

4.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
