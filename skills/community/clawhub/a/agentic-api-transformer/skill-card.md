## Description:

Transform existing API systems to follow the Agentic API Spec design with dynamic discovery and progressive disclosure

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomsun28](https://clawhub.ai/user/tomsun28)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze existing REST or OpenAPI systems, generate agent-friendly response wrappers and discovery entry points, and validate Agentic API compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated middleware or /api/llms.txt discovery output could expose sensitive or authenticated operations if applied without review.

Mitigation: Review generated middleware and discovery output before production use, especially for authenticated or sensitive endpoints.

Risk: API transformation can alter response contracts if applied broadly without validation.

Mitigation: Run compliance checks and inspect generated code before deployment, preserving existing business logic while wrapping responses incrementally.

## Reference(s):

- [Agent API Spec homepage](https://github.com/tomsun28/agent-api-spec)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples, framework code snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review generated middleware and /api/llms.txt output before applying it to production APIs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
