## Description:

Meta-skill for AI agent self-improvement that analyzes runtime logs to detect error patterns, regressions, and inefficiencies, then generates structured improvement proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinasu](https://clawhub.ai/user/sinasu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze agent runtime logs, identify recurring failures or inefficiencies, score system health, and generate prioritized improvement recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input logs may contain secrets, tokens, personal data, or sensitive internal details.

Mitigation: Redact sensitive data before passing logs to the skill.

Risk: Unbounded production or fleet log streams can create operational and data-exposure risk.

Mitigation: Use request-size, runtime, and rate limits before wiring the skill into production or fleet-scale pipelines.

Risk: Rule-based recommendations can miss semantic context or produce incomplete guidance.

Mitigation: Review proposed changes before applying them to agent code or deployment processes.

## Reference(s):

- [Capability Evolver Pro.Bak on ClawHub](https://clawhub.ai/sinasu/skills/capability-evolver-pro-bak)
- [Claw0x](https://claw0x.com)
- [Capability Evolver cloud version](https://claw0x.com/skills/capability-evolver)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON containing detected patterns, health scores, recommendations, evolution proposals, or status details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyze and evolve actions require structured log entries; status returns supported actions, strategies, and limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
