## Description:

Adaptive self-improving agent brain that learns, evolves, and optimizes itself over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eternal0404](https://clawhub.ai/user/eternal0404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record learnings and errors, detect recurring patterns, predict failure risk, and maintain local adaptive guidance across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change future agent behavior through local memory and promoted guidance.

Mitigation: Review learnings and generated guidance before running evolution or adaptation workflows.

Risk: Learning, error, and context text may be stored in long-term local files.

Mitigation: Do not enter secrets, credentials, or sensitive user data into learning or error records.

Risk: Rollback is incomplete if workspace files or ~/.adaptive-brain state are not reviewed.

Mitigation: After rollback, manually inspect workspace guidance files and the ~/.adaptive-brain state directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eternal0404/skills/eternal-adaptive-brain)
- [Publisher profile](https://clawhub.ai/user/eternal0404)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Command-line text, JSON state files, and appended Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local state under ~/.adaptive-brain and may append promoted learnings to OpenClaw workspace Markdown files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
