## Description:

Forces M2.7 to produce an explicit structured plan before writing code, capturing sub-problems, APIs and version requirements, risks, affected files, implementation order, and estimated LOC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephenlthorn](https://clawhub.ai/user/stephenlthorn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to force a structured planning pass before complex implementation work. It is intended for multi-file, higher-LOC, or architecture-sensitive coding tasks where decomposition can reduce wasted generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coding task details and optional retrieved context may be sent to the configured LLM endpoint.

Mitigation: Confirm the endpoint and data-handling expectations before installation, and avoid sending sensitive task context unless approved.

Risk: Generated plans may include incorrect APIs, incomplete file lists, or misleading implementation guidance.

Mitigation: Review the plan before implementation and validate API availability, dependencies, and proposed file changes during normal engineering review.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/stephenlthorn/skills/decompose-plan)
- [Publisher profile](https://clawhub.ai/user/stephenlthorn)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON plan object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The plan includes sub-problems, API requirements, risks, affected files, implementation order, and estimated LOC.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
