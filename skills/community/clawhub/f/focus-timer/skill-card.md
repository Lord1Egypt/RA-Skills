## Description:

Pomodoro-style focus blocks managed by your agent. Start, pause, track sessions. Daily focus time reports. No app needed, just chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to let an agent manage Pomodoro-style focus sessions, breaks, task tagging, and daily or weekly focus summaries through chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write session data to an unrestricted caller-chosen local file path.

Mitigation: Use only in a trusted workspace, avoid exposing the data file path to untrusted input, and prefer a fixed app-owned storage path with deletion controls and visible write errors.

Risk: Local focus-session records may reveal work activity or personal productivity patterns.

Mitigation: Review before installing when local activity privacy matters and keep backups of important local data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/focus-timer)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Conversational text, Markdown examples, JavaScript code, and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local session data to a configured JSON file path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
