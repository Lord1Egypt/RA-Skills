## Description:

Forsy Agent Trace captures authentic AI agent workflows as structured local JSON traces with steps, tools, observations, feedback, failures, artifacts, outcomes, and learning signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forsy](https://clawhub.ai/user/forsy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, evaluators, and workflow owners use this skill to record real agent work as inspectable process traces for workflow review, failure analysis, evaluation construction, and reusable agent work examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated traces can contain private prompts, credentials, personal data, proprietary details, internal URLs, logs, or artifact contents.

Mitigation: Review trace files before sharing or publishing them, and redact or omit sensitive details using consistent placeholders.

Risk: Traces can mislead reviewers if steps, tool calls, outputs, screenshots, or feedback are invented or overclaimed.

Mitigation: Record only actual or reliably reconstructed activity, mark uncertainty in the trace, and use trace mode, validation level, and confidence fields honestly.

## Reference(s):

- [Forsy Agent Trace on ClawHub](https://clawhub.ai/forsy/skills/forsy-agent-trace)
- [Forsy publisher profile](https://clawhub.ai/user/forsy)
- [Forsy Trace repository](https://github.com/Forsy-AI/forsy-trace-skill)
- [Forsy Trace Schema v0.1](schema/forsy_trace_schema_v0_1.json)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [JSON file with structured trace fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local trace records; the open-source version does not require submitting data to Forsy or an external API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
