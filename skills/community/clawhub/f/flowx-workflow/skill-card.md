## Description:

Use when choosing, reusing, naming, building, auditing, inspecting, repairing, evolving, or running FlowX workflows for a user request, including prompt/image/video media workflows, passing inputs, and writing the artifacts FlowX asks a coding agent for.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiechuxi](https://clawhub.ai/user/xiechuxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build and manage FlowX workflows, review and evolve workflow artifacts, and run the resulting services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial, one static analysis was degraded, some references were unresolved, and the declared tool scope is absent.

Mitigation: Review the skill and bundled scripts, and limit environment, file-reading, network, and shell access to what the workflow needs.

Risk: Workflow builds can produce code and services, and real media or service runs can have external effects.

Mitigation: Review generated code before launching a service and authorize side-effecting or billable runs before they start.

## Reference(s):

- [FlowX website](https://www.flow-x.work)

## Skill Output:

**Output Type(s):** [Code, Markdown, JSON configuration, Shell commands, Guidance]

**Output Format:** [Markdown instructions, Python code, JSON workflow configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts follow the current FlowX task contract; media outputs may be files.]

## Skill Version(s):

1.0.13 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
