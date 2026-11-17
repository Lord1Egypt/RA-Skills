## Description:

Monitor AI agent calls, errors, latency, and resource usage with a terminal dashboard and JSON export for observability and metrics tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nantes](https://clawhub.ai/user/nantes)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to add lightweight observability to AI agent workflows, including call counts, error logging, latency tracking, resource snapshots, dashboard views, and local metrics export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Metrics labels, error details, stack traces, and exported files may include secrets, raw prompts, or sensitive operational data.

Mitigation: Run in a least-privileged local Python environment and avoid recording secrets, tokens, raw prompts, or sensitive stack traces in labels or details.

Risk: The skill depends on psutil, which is installed separately by the user.

Mitigation: Pin and review the psutil dependency according to the deployment environment's normal dependency-management process.

Risk: Local JSON and CSV exports may be retained or shared outside the intended environment.

Mitigation: Store exports only in approved locations and apply normal retention, access-control, and cleanup practices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nantes/skills/agent-metrics-osiris)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, JSON, CSV]

**Output Format:** [Markdown guidance with command examples and local JSON or CSV metrics output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local agent_metrics.json by default and can export metrics to JSON or CSV.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
