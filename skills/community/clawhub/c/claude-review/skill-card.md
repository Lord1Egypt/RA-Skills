## Description:

Claude Review is a self-review quality gate that uses Claude CLI to independently review work against the task summary, output context, and optional skill requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paperboardofficial](https://clawhub.ai/user/paperboardofficial)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run an independent Claude CLI review of created or modified work before delivering results. It is intended to catch missed requirements, quality issues, and repeat mistakes against the task context and any skill requirements used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an external Claude CLI with weakened permission checks, and reviewed content may be sent to the Claude service.

Mitigation: Review the exact files or folders before invoking it, avoid directories that may contain secrets, and install the Claude CLI only from a trusted source.

Risk: Review failures can be automatically retained in LESSONS.md for future reviews.

Mitigation: Disable or redirect LESSONS_FILE when review details should not be retained, and avoid including sensitive content in review context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paperboardofficial/skills/claude-review)
- [Publisher profile](https://clawhub.ai/user/paperboardofficial)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with shell command examples and review verdict text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Claude CLI installation and may read files, folders, optional skill context, and an optional lessons file during review.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
