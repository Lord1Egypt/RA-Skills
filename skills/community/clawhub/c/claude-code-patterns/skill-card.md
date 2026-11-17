## Description:

Provides engineering guidance for designing agent scheduling, concurrent tool execution, context compaction, state-machine loops, streaming execution, startup performance, and recoverable-error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siyrs](https://clawhub.ai/user/siyrs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as reference material when designing complex agent systems, including multi-turn conversation loops, tool scheduling, context management, performance optimization, and recovery behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Context compaction patterns may summarize sensitive conversation or tool data.

Mitigation: Redact sensitive conversation and tool data before summarization, and provide user-visible controls for context compaction.

Risk: Examples involving keychain, MDM, memory, Bash, or remote-agent behavior can create broad access if copied directly.

Mitigation: Tightly scope credential, device-management, shell, memory, and remote-agent behavior before adapting snippets into production systems.

Risk: Documentation examples may produce incorrect or misleading implementations when applied without review.

Mitigation: Treat the skill output as design guidance, review adapted code, and test concurrency, context-management, and recovery paths before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/siyrs/skills/claude-code-patterns)
- [Context management reference](artifact/references/context-management.md)
- [State-machine loop reference](artifact/references/state-machine-loop.md)
- [Streaming executor reference](artifact/references/streaming-executor.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown guidance with TypeScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; snippets require review and adaptation before production use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
