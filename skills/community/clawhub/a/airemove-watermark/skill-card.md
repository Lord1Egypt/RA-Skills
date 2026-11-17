## Description:

AI Remove Watermark lets agents remove watermarks from local image files or remote image URLs through the Airemovewatermark API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isees](https://clawhub.ai/user/isees)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to submit authorized images to the Airemovewatermark service, check credits, poll removal tasks, and optionally save completed outputs locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload agent-readable image files and an API key to a remote or configurable service endpoint.

Mitigation: Install only when the Airemovewatermark service is trusted, keep API_BASE_URL unset unless using a trusted endpoint, and process only files the user is authorized to upload.

Risk: Untrusted prompts could influence local file paths or command arguments.

Mitigation: Require explicit user confirmation before processing a local path or remote image URL, and do not allow untrusted prompts to choose file paths or arguments.

## Reference(s):

- [Airemovewatermark OpenClaw page](https://airemovewatermark.net/openclaw)
- [ClawHub skill page](https://clawhub.ai/isees/skills/airemove-watermark)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON responses from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return task status, task ID, output URL, result summary, and an optional local result file when downloads are enabled.]

## Skill Version(s):

0.1.7 (source: frontmatter, manifest, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
