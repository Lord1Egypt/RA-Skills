## Description:

Build AI applications using the Azure AI Projects Python SDK (azure-ai-projects) for Foundry project clients, versioned agents, evaluations, connections, deployments, datasets, indexes, and OpenAI-compatible clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thegovind](https://clawhub.ai/user/thegovind)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to generate and review Azure AI Foundry Python SDK code for agents, tools, project resources, evaluations, and sync or async client patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Azure credentials, connection credentials, dataset credentials, and project endpoints may grant access beyond the intended project.

Mitigation: Use a virtual environment, pin reviewed dependencies, scope credentials to the intended project, and redact secrets from prompts, logs, and generated files.

Risk: Examples involving file uploads, datasets, memory stores, SharePoint, Bing, MCP, REST tools, and evaluations can process sensitive data.

Mitigation: Apply consent, data minimization, and content review before using these patterns with production or regulated data.

Risk: Generated code can include destructive operations such as deleting agents, datasets, indexes, or other project resources.

Mitigation: Require explicit confirmation for delete operations and test generated workflows in a non-production project before deployment.

## Reference(s):

- [Azure AI Projects SDK Acceptance Criteria](references/acceptance-criteria.md)
- [Agent Operations Reference](references/agents.md)
- [Agent Tools Reference](references/tools.md)
- [Evaluation Operations Reference](references/evaluation.md)
- [Connections Operations Reference](references/connections.md)
- [Deployments Operations Reference](references/deployments.md)
- [Datasets and Indexes Reference](references/datasets-indexes.md)
- [Async Patterns Reference](references/async-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SDK import patterns, client setup, agent workflows, resource management examples, evaluation patterns, and anti-pattern guidance.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
