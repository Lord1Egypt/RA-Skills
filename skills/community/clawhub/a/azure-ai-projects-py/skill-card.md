## Description: <br>
Build AI applications using the Azure AI Projects Python SDK (azure-ai-projects). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegovind](https://clawhub.ai/user/thegovind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build Azure AI Foundry applications with the Azure AI Projects Python SDK, including project clients, versioned agents, tools, threads, runs, connections, deployments, datasets, indexes, evaluations, and async patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples can interact with Azure AI Foundry resources and may require credentials, project endpoints, deployments, datasets, indexes, or external connections. <br>
Mitigation: Use a virtual environment, confirm the Azure project endpoint and deployment names, and run examples only with least-privilege Azure roles. <br>
Risk: Some documented APIs can return or include credentials, especially include_credentials=True and dataset credential flows. <br>
Mitigation: Request credentials only when necessary, and never print, log, serialize, or send returned secrets to an agent or model prompt. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thegovind/azure-ai-projects-py) <br>
- [Agents Reference](references/agents.md) <br>
- [Tools Reference](references/tools.md) <br>
- [Evaluation Reference](references/evaluation.md) <br>
- [Connections Reference](references/connections.md) <br>
- [Deployments Reference](references/deployments.md) <br>
- [Datasets and Indexes Reference](references/datasets-indexes.md) <br>
- [Async Patterns Reference](references/async-patterns.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples may require Azure credentials, project endpoints, model deployments, and least-privilege Azure roles.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
