## Description:

Trace and debug a single OpenClaw conversation session. Use when you need to analyze openclaw logs, correlate them with the current session context, inspect workflow steps, summarize module activity, or produce a structured trace report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leoluo0814](https://clawhub.ai/user/leoluo0814)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use ClawTrace to inspect one OpenClaw session, correlate local JSON logs with current session context, reconstruct workflow steps, and produce an evidence-based trace report with optimization suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw logs and session context can expose operational details from a run.

Mitigation: Use the skill only for sessions the reviewer is authorized to inspect, and review generated reports before sharing.

Risk: Partial or truncated logs can produce incomplete timing, step, warning, or error analysis.

Mitigation: State when logs are partial and mark unsupported metrics or durations as Not available, Estimated, or Unknown.

## Reference(s):

- [ClawTrace skill page](https://clawhub.ai/leoluo0814/skills/clawtrace)

## Skill Output:

**Output Type(s):** [markdown, guidance, shell commands]

**Output Format:** [Markdown report, either as a file or direct chat response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should avoid raw logs, raw JSON, and verbatim log lines; missing values are marked as Not available, Estimated, or Unknown.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
