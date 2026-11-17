## Description:

Use when managing Function Compute AgentRun resources via OpenAPI, including runtime, sandbox, model, memory, credential, endpoint, status, and troubleshooting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud Function Compute AgentRun runtimes, endpoints, sandboxes, model services, memory, and credentials through OpenAPI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials can authorize changes to Alibaba Cloud AgentRun resources.

Mitigation: Use least-privilege RAM credentials and short-lived security tokens when available.

Risk: Incorrect endpoints or regions can operate on unintended resources.

Mitigation: Verify AGENTRUN_ENDPOINT and the target region before running workflows.

Risk: The cleanup workflow deletes the specified runtime endpoint and runtime.

Mitigation: Confirm AGENTRUN_RUNTIME_ID and AGENTRUN_RUNTIME_ENDPOINT_ID before executing cleanup_runtime.py.

Risk: Generated response JSON may contain resource identifiers or operational details.

Mitigation: Review output JSON before sharing or storing it outside the intended evidence directory.

## Reference(s):

- [AgentRun OpenAPI API Overview](references/api_overview.md)
- [AgentRun OpenAPI Service Endpoints](references/endpoints.md)
- [AgentRun SDK Guidance](references/sdk.md)
- [Source List](references/sources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON response file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may save Alibaba Cloud API response JSON under output/compute-fc-agentrun/responses.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
