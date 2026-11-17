## Description:

Manages MCP dependency graphs, topological ordering, circuit-breaker states, failure and success recording, resets, bulkhead status, cascade analysis, and post-deployment validation for resilience operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to register MCP dependencies, inspect circuit-breaker health, record call outcomes, reset breaker state after remediation, and analyze cascading failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: State-changing actions such as register, reset, record_failure, and record_success can alter resilience-mcp behavior.

Mitigation: Run state-changing actions only in environments where circuit-breaker management is intended and only with explicit operator direction.

Risk: Incorrect dependency registrations or resets can affect MCP startup ordering, fallback behavior, or fault isolation.

Mitigation: Review target MCP names, dependency lists, and current circuit state before applying changes, then verify health and dependency graph output afterward.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/circuit-breaker-manager)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON request and response examples, command-line examples, and operational recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operational actions may change resilience-mcp dependency and circuit-breaker state.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
