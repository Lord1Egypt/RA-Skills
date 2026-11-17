## Description:

Guides an agent to preserve task state in a handoff file and memory notes before a context reset or task change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzyyj](https://clawhub.ai/user/lzyyj)

### License/Terms of Use:

MIT-0

## Use Case:

People using long-running assistants can preserve work in progress and resume it in a fresh session without manually reconstructing task context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Handoff and memory files can retain sensitive task or environment details.

Mitigation: Use the workflow only where local persistence is intended, and do not put secrets in generated files.

Risk: A stale handoff can cause a later session to resume an obsolete task.

Mitigation: Clear or delete HANDOFF.md after the task is complete.

## Reference(s):

- [Context Rotation on ClawHub](https://clawhub.ai/lzyyj/skills/context-rotation)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown handoff and memory files, plus a brief user-facing message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The handoff is temporary; daily logs and curated memory can persist across sessions.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
