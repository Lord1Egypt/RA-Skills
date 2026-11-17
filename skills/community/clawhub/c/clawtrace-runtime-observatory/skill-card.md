## Description:

ClawTrace Runtime Observatory observes, reconstructs, records, and explains AI workflow behavior at runtime without modifying workflows, outputs, retries, fallback behavior, or orchestration decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect runtime traces, reconstruct workflow chains, and diagnose retry, fallback, critic, arbitration, and context-integrity behavior in agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime traces and previous outputs may expose sensitive workflow context.

Mitigation: Install only where users are authorized to inspect traces, and redact secrets or private context before exposing trace output.

Risk: Vague or automatic debug triggers may reveal broader workflow details than intended.

Mitigation: Prefer explicit diagnostic commands and trusted debug-mode metadata before enabling trace output.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON diagnostics with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs workflow reconstruction, trace summaries, context integrity status, system health, and trace-scoped retry requests when logs are missing.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
