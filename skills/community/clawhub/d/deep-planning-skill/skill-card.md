## Description:

Deep Planning guides an agent through a high-latency planning workflow for complex architecture, algorithm, system-design, logic, or research-planning tasks and produces a self-contained execution blueprint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobertneek](https://clawhub.ai/user/bobertneek)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and research agents use this skill to create robust execution blueprints before complex implementation, architecture, algorithm, logic, or research-planning work begins. It is intended for high-complexity planning tasks where ordinary linear planning may miss constraints, failure modes, or alternative mechanisms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add latency and additional subagent or model usage because it performs an expanded planning workflow.

Mitigation: Use it for complex architecture, algorithm, system-design, logic, or research-planning tasks; use normal tactical workflows for routine bug fixes, simple refactors, factual lookup, and straightforward API usage.

Risk: If subagent isolation is unavailable, the Domain Questioner step is lower confidence because true blank-context separation did not occur.

Mitigation: Clearly label simulated Domain Questioner results as lower confidence and preserve the context-separation rules as much as the environment allows.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown blueprint with structured sections, scorecards, validation steps, logs, and final receipt requirements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only workflow; may increase latency and subagent or model usage when a real Domain Questioner is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
