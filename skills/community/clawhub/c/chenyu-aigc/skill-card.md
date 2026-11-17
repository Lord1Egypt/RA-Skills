## Description:

Generate AI videos and images via the Chenyu Studio AIGC API, including text-to-video, image-to-video, video extension, style transfer, and AI image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dionren](https://clawhub.ai/user/dionren)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover Chenyu AIGC recipes, submit video or image generation tasks, and poll or manage resulting outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can send API keys and private prompts, images, videos, or audio to a configurable endpoint.

Mitigation: Use only a trusted HTTPS CHENYU_BASE_URL, preferably the documented default, and a narrowly scoped Chenyu API key; do not submit sensitive media or prompts unless the configured provider is acceptable.

Risk: The local image example writes a base64 payload to a predictable temporary file.

Mitigation: Use a private secure temporary file for local media payloads and remove it after upload.

Risk: Completed task deletion may be irreversible.

Mitigation: Confirm retention requirements before deleting generated tasks or outputs.

## Reference(s):

- [Execute a Recipe](execute-recipe.md)
- [Manage Tasks](manage-tasks.md)
- [Chenyu API Base URL](https://chenyu.pro)
- [ClawHub Skill Page](https://clawhub.ai/dionren/skills/chenyu-aigc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces API usage guidance for recipe discovery, task submission, polling, cancellation, listing, and deletion.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
