## Description: <br>
Routes tasks to cost-effective capable models, handles provider failures, and keeps model routing configuration current. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adroidian](https://clawhub.ai/user/adroidian) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to choose an appropriate model tier for delegated work, retry after rate limits, inspect model health and costs, and maintain routing configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The provider sync script reads local provider credentials and can contact external or private provider endpoints. <br>
Mitigation: Review the sync behavior before installation, run dry-run mode first, and only enable providers and endpoints that are approved for the deployment environment. <br>
Risk: The bundled sync workflow can mutate routing configuration and send model-change notifications to a hard-coded Telegram destination. <br>
Mitigation: Replace or disable the Telegram configuration and review generated config changes before enabling scheduled or live sync runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adroidian/chitin-core) <br>
- [Publisher profile](https://clawhub.ai/user/adroidian) <br>
- [Chitin homepage](https://chitin.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON command results and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Router commands return structured model-selection, failure, health, cost, and validation information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
