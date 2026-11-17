## Description:

OpenClaw communication protocol architecture optimization skill package that provides a high-performance agent communication framework with large-message performance improvements, MessagePack size reduction, unified transport architecture, smart routing, error recovery, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[21b-a](https://clawhub.ai/user/21b-a)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add or evaluate an OpenClaw agent-to-agent communication layer with unified send, request-response, and broadcast APIs. It is intended for communication architecture optimization work involving transport selection, protocol serialization, retry behavior, and performance monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scan verdict is suspicious because the skill overstates production-ready communication while persisting messages to weakly scoped filesystem paths and reporting simulated transports or protocols as successful.

Mitigation: Review carefully before installing in any real agent workflow and use only in a disposable or test environment until recipient identifiers are validated, writable paths are sandboxed, MessagePack is disabled or replaced with a real implementation, and HTTP/WebSocket behavior is made fail-closed or clearly test-only.

## Reference(s):

- [OpenClaw homepage](https://openclaw.ai)
- [Skill page](https://clawhub.ai/21b-a/skills/arch-optimization)
- [Transport layer design](artifact/docs/transport-layer-design.md)
- [Protocol layer design](artifact/docs/protocol-layer-design.md)
- [Performance comparison results](artifact/reports/performance-comparison-results.json)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation with JavaScript code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes implementation files, design notes, examples, tests, and performance reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
