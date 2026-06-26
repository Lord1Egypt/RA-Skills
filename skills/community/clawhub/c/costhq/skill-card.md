## Description: <br>
Track agent session costs, file changes, git commits, local model usage, budgets, and audit activity with the CostHQ CLI and dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brian-mwirigi](https://clawhub.ai/user/brian-mwirigi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use CostHQ to start, monitor, annotate, and end tracked work sessions while recording AI usage, file changes, git commits, budgets, and dashboard analytics. It is especially relevant for teams that need local model cost tracking, semantic caching controls, exports, or enterprise audit trails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CostHQ records session, file, git, and AI-traffic activity with under-specified privacy and retention controls. <br>
Mitigation: Review what the npm package records, where sync features send data, how local data under ~/.costhq or ~/.CostHQ is purged, and whether the data handling fits the repository or regulatory environment before use. <br>
Risk: The Semantic Caching Proxy can intercept and cache model traffic, which may include prompts, responses, or credentials. <br>
Mitigation: Avoid enabling the proxy for secrets or confidential model traffic unless cache isolation, retention, and credential handling are clear. <br>


## Reference(s): <br>
- [CostHQ on ClawHub](https://clawhub.ai/brian-mwirigi/costhq) <br>
- [CostHQ GitHub Repository](https://github.com/brian-mwirigi/costhq) <br>
- [CostHQ npm Package](https://www.npmjs.com/package/costhq) <br>
- [CostHQ Changelog](https://github.com/brian-mwirigi/costhq/blob/main/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash command blocks and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agents are instructed to use --json for parseable CostHQ command output.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata and skill body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
