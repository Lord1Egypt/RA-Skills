## Description:

Autonomous Science Loop helps agents fit candidate laws to observations, design follow-up experiments, refute inconsistent hypotheses, and return the simplest supported law.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users can use this skill to explore numeric observations, compare simple candidate models, and produce an experiment trace for active learning or model selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The learner module can persist usage history, errors, free-form notes, and preferences across sessions.

Mitigation: Review the learner behavior before installation and disable or remove local memory persistence if cross-session memory is not desired.

Risk: The skill instructions encourage lessons to be written back into SKILL.md after repeated errors or usage.

Mitigation: Require human review for changes to the skill definition and avoid automated self-modification in managed deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/autonomous-science-loop)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python examples; runtime science-loop reports are JSON-compatible dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local learned_patterns.json memory when the learner module is used.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
