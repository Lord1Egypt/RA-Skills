## Description:

Manage Function Compute AgentRun resources via OpenAPI for runtime, sandbox, model, memory, and credential workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud Function Compute AgentRun runtimes, endpoints, sandboxes, model services, memory collections, and credentials through OpenAPI-backed workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Alibaba Cloud credentials for AgentRun resource operations.

Mitigation: Use short-lived, least-privilege RAM credentials and avoid sharing generated response files that may contain cloud metadata.

Risk: Cleanup workflows can delete AgentRun runtime endpoints and runtimes.

Mitigation: Verify the account, region, runtime ID, and endpoint ID before running cleanup_runtime.py.

Risk: Endpoint selection is user-controlled and weakly scoped.

Mitigation: Set AGENTRUN_ENDPOINT only to an official endpoint listed in references/endpoints.md.

## Reference(s):

- [AgentRun API Overview](references/api_overview.md)
- [AgentRun OpenAPI Endpoints](references/endpoints.md)
- [AgentRun SDK Guidance](references/sdk.md)
- [Source List](references/sources.md)
- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/alicloud-compute-fc-agentrun)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands, Python script references, and JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated API response summaries under output/compute-fc-agentrun/responses.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
