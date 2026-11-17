## Description:

Collects and processes user feedback on task completion. Use after important tasks to ask if the result was satisfactory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wqz666](https://clawhub.ai/user/wqz666)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users use this skill after important tasks to ask whether the result was satisfactory, capture quick or detailed feedback, and update feedback or preference notes for future interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent feedback and preference notes can steer future agent behavior without enough scoping or deletion controls.

Mitigation: Require explicit user consent before saving feedback, constrain where notes are stored, and periodically review or delete memory files.

Risk: Outdated or misleading saved feedback can cause the agent to preserve unhelpful behavior patterns.

Mitigation: Treat saved feedback as editable user preference data and confirm important behavior changes before relying on it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wqz666/skills/feedback-collector)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prompts and feedback log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language prompts; may produce persistent local feedback and preference notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
