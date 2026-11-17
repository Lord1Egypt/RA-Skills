## Description:

AICE tracks bidirectional confidence for agents, users, and teams across TECH, OPS, JUDGMENT, COMMS, and ORCH domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brugillo](https://clawhub.ai/user/brugillo)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to score agent behavior, user input quality, and team coordination during ongoing agent work. It supports confidence tracking, correction patterns, task-completion scoring, and optional Hub synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for durable authority through confidence scoring and optional Hub sync.

Mitigation: Review before installing, keep persistence and Hub sync explicit opt-in, and do not grant authority beyond the intended confidence-scoring workflow.

Risk: Default or example state can be misleading if reused as live confidence data.

Mitigation: Reset the starter template to a neutral unregistered state and remove personal example data before deployment.

Risk: Protected prompts or private context could be exposed if the skill is over-granted access.

Mitigation: Do not allow the skill to read protected prompts or install enforcement hooks or plugins automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brugillo/skills/aice)
- [AICE reference](resources/AICE_REFERENCE.md)
- [AICE user scoring](resources/AICE_USER_SCORING.md)
- [Evaluator guide](resources/EVALUATOR_GUIDE.md)
- [Triggers and patterns](resources/TRIGGERS_AND_PATTERNS.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces confidence scores, scoring rationale, operational guidance, and starter configuration; Hub sync is optional and explicit.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
