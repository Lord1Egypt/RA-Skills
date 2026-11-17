## Description:

Capability Evolver Pro analyzes agent runtime logs to detect error patterns, regressions, and inefficiencies, then generates structured improvement proposals for reliability, diagnosis, and health assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackey001-wq](https://clawhub.ai/user/jackey001-wq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to analyze structured agent logs, diagnose recurring failures, assess system health, and generate prioritized improvement proposals for agent reliability workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production logs may contain tokens, credentials, personal data, or sensitive URLs.

Mitigation: Redact sensitive values before analysis and avoid submitting logs that exceed the runtime's approved data-handling policy.

Risk: Very large or malformed log batches may create reliability issues if the runtime does not enforce request size and schema limits.

Mitigation: Apply request validation, schema checks, and batch-size limits before invoking analyze or evolve actions.

Risk: Pattern-based recommendations can be incomplete or misleading when the log structure omits important operational context.

Mitigation: Have engineers review recommendations before applying changes, especially for production incident response or automated improvement pipelines.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jackey001-wq/skills/capability-evolver-pro-1-0-2)
- [Publisher Profile](https://clawhub.ai/user/jackey001-wq)
- [Claw0x Capability Evolver Page](https://claw0x.com/skills/capability-evolver)
- [Declared Project Link](https://github.com/kennyzir/capability-evolver)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON results with diagnostic text, scores, patterns, recommendations, and proposal objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by action: analyze returns patterns, health score, recommendations, and summary; evolve returns prioritized recommendations, risk assessment, and estimated improvement; status returns supported actions, strategies, and limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
