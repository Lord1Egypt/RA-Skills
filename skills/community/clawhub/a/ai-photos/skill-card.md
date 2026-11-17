## Description:

AI Photos turns local photo folders into a searchable AI photo album for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoubingwu](https://clawhub.ai/user/zoubingwu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use AI Photos to create, reconnect, search, and optionally auto-index local photo albums in OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs the latest GitHub release binary without integrity verification.

Mitigation: Install only when the publisher is trusted, review the release source before use, and prefer a pinned or independently verified binary where policy requires it.

Risk: Photo libraries may contain sensitive personal data, and prepared images may be sent to a vision model for captioning.

Mitigation: Use only folders the user explicitly chooses, explain the image processing path, and avoid shared OS accounts or workspaces for private albums.

Risk: Automatic indexing can periodically scan selected folders in the background.

Mitigation: Enable automatic indexing only after explicit user approval; keep manual indexing when background scanning is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoubingwu/skills/ai-photos)
- [ai-photos CLI repository](https://github.com/zoubingwu/openclaw-ai-photos)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks and JSONL record descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local album setup/search actions, captioned JSONL records, heartbeat instructions, and local gallery handoff text.]

## Skill Version(s):

2.2.0 (source: server release metadata; skill frontmatter metadata v2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
