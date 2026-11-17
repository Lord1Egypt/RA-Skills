## Description:

Helps AI coding agents instrument AI/LLM applications with the Anyway observability SDK for tracing, monitoring, and cost tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremy-any](https://clawhub.ai/user/jeremy-any)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to have coding agents add Anyway SDK setup, environment configuration, and tracing instrumentation to Python or JavaScript applications that call LLM providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic instrumentation may export prompts, responses, metadata, or other LLM telemetry to an external collector.

Mitigation: Confirm collection scope, retention, access controls, and redaction settings before enabling the SDK in projects with sensitive data.

Risk: Broad provider auto-instrumentation can capture more application behavior than intended.

Mitigation: Use narrower instrumentation or explicit workflow and task spans when full automatic tracing is not appropriate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeremy-any/skills/anyway-traces)
- [Anyway Documentation Index](https://docs.anyway.sh/llms.txt)
- [Anyway Skill File](https://docs.anyway.sh/skills.md)
- [Anyway Quickstart](https://docs.anyway.sh/quickstart)
- [Python SDK Installation](https://docs.anyway.sh/sdk/python/installation)
- [Python SDK Configuration](https://docs.anyway.sh/sdk/python/configuration)
- [Python SDK Tracing](https://docs.anyway.sh/sdk/python/tracing)
- [JavaScript SDK Installation](https://docs.anyway.sh/sdk/js/installation)
- [JavaScript SDK Configuration](https://docs.anyway.sh/sdk/js/configuration)
- [JavaScript SDK Tracing](https://docs.anyway.sh/sdk/js/tracing)

## Skill Output:

**Output Type(s):** [code, configuration, guidance, shell commands]

**Output Format:** [Markdown guidance with code and configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit language-specific setup instructions for Python or JavaScript projects.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
