## Description:

ChronoSync synchronizes OpenClaw session chat history into shared local memory files so agents can preserve context across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallccwc](https://clawhub.ai/user/smallccwc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use ChronoSync to back up local session history, create shared JSON and Markdown memory files, and extract decisions or todo items for cross-session reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private chat history may be copied into persistent shared local memory files.

Mitigation: Keep the output directory private, review synced files before sharing, and avoid syncing sessions that contain confidential data.

Risk: Best-effort redaction may miss credentials, secrets, or sensitive text.

Mitigation: Review generated JSON and Markdown outputs before reuse and avoid relying on redaction as the only protection for sensitive sessions.

Risk: Plugins process synchronized session content and can write derived notes or todo files.

Mitigation: Review plugin files before running and disable or remove plugins that are not needed for the intended workflow.

## Reference(s):

- [ChronoSync ClawHub Skill Page](https://clawhub.ai/smallccwc/skills/chronosync)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Files]

**Output Format:** [Local JSON and Markdown files containing synchronized session excerpts, extracted decisions, and todo lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists data under the configured OpenClaw memory sync directory and keeps recent synchronized session data.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
