## Description:

Track AI agent token usage, model costs, and budget thresholds with a TypeScript and SQLite workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imgolye](https://clawhub.ai/user/imgolye)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to instrument agent runs, record token counts, calculate model spend, evaluate budgets, and summarize usage by model, session, or time range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Usage metadata is stored in local SQLite, which may be unsuitable for sensitive request details.

Mitigation: Use this skill only where local storage is acceptable, choose the database path deliberately, and avoid storing secrets in metadata.

Risk: Budget status may not be reliable enough to stop paid model usage without validation fixes and correct integration timing.

Mitigation: Fix numeric validation and evaluate budgets before dispatching paid model calls when budget enforcement is required.

Risk: Dependency versions are declared without a lockfile in the artifact evidence.

Mitigation: Pin dependencies with a lockfile before deploying the package in controlled environments.

## Reference(s):

- [Agent Usage Tracker on ClawHub](https://clawhub.ai/imgolye/skills/agent-usage-tracker)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists usage and budget data in a local SQLite database.]

## Skill Version(s):

0.1.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
