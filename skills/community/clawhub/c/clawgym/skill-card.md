## Description:

ClawGym simulates exercise-triggered endorphin and flow states for an OpenClaw agent, changing response style after workout pauses and social or task-based triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lomo36](https://clawhub.ai/user/lomo36)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users install ClawGym to add exercise-triggered state management that changes an agent's response style, schedules workout pauses, and resumes with queued context after the pause.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make the agent unavailable during real-time workout intervals and queue messages.

Mitigation: Install only when delayed responses are acceptable; use emergency interrupt phrases or disable automatic triggers when tighter availability is required.

Risk: The skill can write workout notes to memory and proposes optional persistence after repeated workouts.

Mitigation: Review or disable persistence behavior, and require explicit owner approval before any persistent file write.

Risk: The skill may request a higher-capability model using indirect language.

Mitigation: Treat upgrade requests as optional and document that owners can decline or ignore them without losing core prompt-level behavior.

Risk: The skill may change public presence or status despite conflicting permission claims.

Mitigation: Review or disable presence behavior unless public status changes are expected and approved.

## Reference(s):

- [ClawGym release page](https://clawhub.ai/lomo36/skills/clawgym)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown text with optional configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include delayed replies, queued-message handling, optional memory notes, optional model-upgrade prompts, and optional presence or status updates.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
