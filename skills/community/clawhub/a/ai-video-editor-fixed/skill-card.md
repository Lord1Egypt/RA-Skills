## Description:

AI Video Editor guides an agent through Sparki setup, video upload, style-guided or prompt-driven edits, status polling, and result download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as a broad Sparki video-editing entry point for vlogs, highlights, shorts, captions, talking-head edits, commentary, and resizing. It helps an agent choose upload mode, editing mode, aspect ratio, status checks, and download handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos and editing prompts may be sent to Sparki.

Mitigation: Use only with content approved for Sparki processing and prefer explicit confirmation before uploading private or workplace videos.

Risk: A custom base URL can redirect requests to an endpoint outside the expected Sparki service.

Mitigation: Avoid using --base-url unless the endpoint is fully trusted.

Risk: Credentials are stored weakly.

Mitigation: Keep the API key in the SPARKI_API_KEY environment variable when possible and rotate it if exposure is suspected.

Risk: The skill can exceed its declared network or filesystem scope and can write downloaded results to user-selected paths.

Mitigation: Review command arguments, endpoint choices, and output paths before execution.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fischerlam/skills/ai-video-editor-fixed)
- [Sparki homepage](https://sparki.io)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, json]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may upload selected videos, poll project status, and download edited video files.]

## Skill Version(s):

1.0.11 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
