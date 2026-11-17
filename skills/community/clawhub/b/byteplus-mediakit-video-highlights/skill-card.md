## Description:

Create and query BytePlus/MediaKit video highlight editing tasks with the video-highlights-llm tool, focused on preset-based football highlight reels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bpvnebot](https://clawhub.ai/user/bpvnebot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media workflow operators use this skill to submit and query asynchronous BytePlus MediaKit football highlight reel tasks from one or more HTTP/HTTPS video URLs, with optional scoring prompts, analysis prompts, callbacks, and target durations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script can send API credentials and task data to a configured endpoint.

Mitigation: Keep the endpoint pinned to the documented BytePlus HTTPS host unless intentionally using an approved internal environment.

Risk: Diagnostics can expose custom secret-bearing headers.

Mitigation: Avoid storing secrets in custom headers and treat doctor output as potentially sensitive when custom headers are configured.

Risk: The skill requires MediaKit credentials to submit or query tasks.

Mitigation: Configure API keys outside chat using environment or local config mechanisms and avoid pasting raw keys into conversations.

## Reference(s):

- [video-highlights-llm API Notes](artifact/references/api.md)
- [Request Templates](artifact/references/templates.md)
- [ClawHub skill page](https://clawhub.ai/bpvnebot/skills/byteplus-mediakit-video-highlights)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task IDs, query status, output durations, and generated highlight video URLs when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
