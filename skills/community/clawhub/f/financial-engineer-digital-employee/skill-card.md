## Description: <br>
覆盖数据探查、单变量分析、特征工程、LR评分卡、XGBoost/DNN建模、超参数调优、模型解释、多模型对比、分群建模、DeepModel集成全流程。从数据到模型上线的一站式机器学习建模能力。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gechengling](https://clawhub.ai/user/gechengling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial analysts, risk modelers, and agent operators use this skill to plan or run data profiling, univariate analysis, feature engineering, scorecard modeling, XGBoost/DNN workflows, tuning, model explanation, model comparison, segmentation, and ensemble modeling for financial datasets. Outputs should be reviewed by qualified humans before they are used for business, financial, legal, insurance, or customer-impacting decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to process financial or customer datasets, train models, and write model or report artifacts to disk. <br>
Mitigation: Approve the exact data path, output directory, retention plan, and whether AUTO tuning or autonomous experiments are allowed before use. <br>
Risk: Regulated, PII-bearing, confidential, or customer-impacting data could be processed without an adequate governance decision. <br>
Mitigation: Do not use such data unless the data owner has approved the workflow, storage location, retention policy, and human review process. <br>
Risk: Modeling results or financial analysis could be mistaken for professional financial, legal, insurance, or business advice. <br>
Mitigation: Treat outputs as analytical guidance only and require qualified human review before any real-world decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gechengling/financial-engineer-digital-employee) <br>
- [Publisher profile](https://clawhub.ai/user/gechengling) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe reports, model artifacts, metrics, and result manifests produced by local financial ML workflows.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
