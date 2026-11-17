## Description:

Agent observability, tracing, and metrics guidance for trace IDs, spans, event taxonomy, secret redaction, latency and bottleneck analysis, retry analysis, incident timelines, health scoring, and cross-skill diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to structure observability for agent workflows, including logging, tracing, metrics, failure diagnosis, retry tracking, incident reporting, and privacy-aware operational summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Observability traces may capture credentials, tokens, private prompts, or personal data if deployed without controls.

Mitigation: Keep secret redaction always enabled, avoid raw prompt logging by default, minimize stored data, and apply scoped retention to trace storage.

Risk: Diagnostic reports may overstate root cause, success, or regression findings when evidence is incomplete.

Mitigation: Use explicit confidence labels, require verification before declaring success, and distinguish confirmed root causes from likely or possible causes.

Risk: Retry and recovery guidance can create noisy traces or repeated failures if implemented without limits.

Mitigation: Use bounded retries with backoff, flag retry loops, and change strategy or stop when repeated attempts make no progress.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with structured trace, event, metric, diagnostic, and incident-report patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; emphasizes secret redaction, minimal raw-prompt logging, bounded retries, and evidence-based diagnostic confidence.]

## Skill Version(s):

1.1.0 (source: artifact/_meta.json, SKILL.md metadata.openclaw.version, evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
