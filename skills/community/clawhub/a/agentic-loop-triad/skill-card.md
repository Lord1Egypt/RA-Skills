## Description:

Unifies intent-engineering, execution, and feedback into an autonomous loop that detects drift, learns patterns, adjusts specs, transfers skills, and produces auditable improvement artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run an autonomous improvement loop over goals, specifications, outcomes, and feedback. It is intended to produce specifications, analysis, regression tests, run reports, revised criteria, and cross-cycle learning artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist run history and learning artifacts that may contain goal details, outcomes, or operational context.

Mitigation: Use a dedicated output directory and review generated artifacts before sharing, retaining, or reusing them.

Risk: The skill may automatically revise success criteria, which can change the standard used to judge whether a goal was met.

Mitigation: Review generated revised_specification.json before relying on it, and use --no-auto-revise for important targets that require fixed criteria.

Risk: The improvement chain should not be treated as tamper-proof audit evidence.

Mitigation: Use the chain as local traceability support only, and keep independent review or audit controls for high-stakes governance claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielfoojunwei/skills/agentic-loop-triad)
- [Integration Guide](artifact/references/integration_guide.md)
- [Paradigm Shifts Reference](artifact/references/paradigm_shifts_reference.md)
- [Pipeline Configuration](artifact/references/pipeline_config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python CLI commands and JSON or Markdown run artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent run artifacts to the selected output directory, including pipeline state, analysis, improvement reports, learning logs, and optional revised specifications.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
