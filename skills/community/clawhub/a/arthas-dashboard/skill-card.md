## Description:

Arthas Dashboard formats Arthas JVM diagnostics into monitoring views for threads, memory, GC, method calls, and related health checks with anomaly detection and suggested fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnyzuo](https://clawhub.ai/user/johnnyzuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect JVM health through Arthas MCP tools, summarize runtime metrics, detect likely anomalies, and receive practical remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic output may expose sensitive runtime data such as environment variables, system properties, method arguments, credentials, or live business data.

Mitigation: Install only for authorized JVM targets, scope watch/sysenv/sysprop usage carefully, and sanitize outputs before sharing or retaining conversations or logs.

Risk: Trace, watch, monitor, and profiler diagnostics can affect target JVM performance when used on busy production paths.

Mitigation: Use focused targets, stop sampling promptly after diagnosis, and prefer low-impact read-only checks before deeper instrumentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnyzuo/skills/arthas-dashboard)
- [Server-resolved GitHub provenance](https://github.com/johnnyzuo/arthas-dashboard/tree/main/arthas-dashboard)
- [ClawHub publisher profile](https://clawhub.ai/user/johnnyzuo)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance, analysis]

**Output Format:** [Markdown tables, dashboard-style text reports, command suggestions, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive diagnostic values from live JVM runtime data when Arthas tools return them.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
