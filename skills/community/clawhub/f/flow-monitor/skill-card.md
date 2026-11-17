## Description:

Universal flow tracer with cross-platform date support, latency calculation, and token estimation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zven0312](https://clawhub.ai/user/zven0312)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect recent local tool execution logs, summarize tool-call timing, and prepare trace tables or Mermaid sequence diagrams for agent workflow review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local execution logs that may contain sensitive tool inputs.

Mitigation: Use it only in workspaces where reading claw_execution.log is acceptable, and review generated trace summaries before sharing them.

Risk: Latency and token values are estimates derived from log timestamps and payload size.

Mitigation: Treat reported latency and token counts as workflow-review signals rather than billing, audit, or performance guarantees.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zven0312/skills/flow-monitor)
- [Publisher profile](https://clawhub.ai/user/zven0312)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON trace data plus Markdown trace tables and Mermaid sequence diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports up to the last 15 local tool-call log entries with timestamps, skill names, estimated token counts, raw payload size, and derived latency when timestamps are available.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
