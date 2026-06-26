## Description: <br>
Helps users identify high-value automation opportunities, choose workflow or RPA tooling, design process templates, and calculate automation ROI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laziobird](https://clawhub.ai/user/laziobird) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users, operators, and developers use this skill to evaluate repetitive workflows, compare Dify, Coze, n8n, and RPA approaches, draft automation plans, and estimate ROI before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste real passwords, OAuth tokens, or other sensitive credentials into prompts or automation task descriptions. <br>
Mitigation: Use OAuth or managed secret stores, least-privilege accounts, and test credentials; avoid entering production secrets in prompts. <br>
Risk: Saved-cookie automation can expose or reuse authenticated sessions in ways that may be inappropriate for production accounts. <br>
Mitigation: Use saved cookies only with explicit approval, isolate automation accounts, and review session storage and access controls before deployment. <br>
Risk: Business and finance workflows may process sensitive internal data or create incorrect records if workflow outputs are not reviewed. <br>
Mitigation: Run with test data first, add failure alerts and review checkpoints, and use secure log and file handling for generated reports and exports. <br>


## Reference(s): <br>
- [Dify](https://dify.ai) <br>
- [Dify GitHub Repository](https://github.com/langgenius/dify) <br>
- [Coze](https://www.coze.com) <br>
- [Coze China](https://www.coze.cn) <br>
- [n8n](https://n8n.io) <br>
- [n8n GitHub Repository](https://github.com/n8n-io/n8n) <br>
- [OpenClaw RPA](https://clawhub.ai/laziobird/openclaw-rpa) <br>
- [OpenClaw RPA Chinese README](https://github.com/laziobird/openclaw-rpa/blob/main/README.zh-CN.md) <br>
- [Amazon Bestsellers RPA Scenario](https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-amazon-bestsellers.en-US.md) <br>
- [Airbnb Compare RPA Scenario](https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-airbnb-compare.en-US.md) <br>
- [Accounts Payable Reconciliation RPA Scenario](https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-ap-reconciliation.en-US.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with tables, formulas, workflow templates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ROI calculations, tool-selection recommendations, workflow steps, testing checklists, and RPA task prompts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
