## Description:

BBDuck helps agents compress local JPG, PNG, WEBP, and GIF images with a visual-lossless default, streaming compression logs, and optional ZIP downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoolee](https://clawhub.ai/user/zhaoolee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use BBDuck to compress local images through a local Docker-backed API while preserving visual quality and observing stream logs. It is suited for single-image compression workflows and packaging completed outputs into a ZIP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned third-party Docker image that may change over time.

Mitigation: Review the Docker service before installing and prefer a pinned image digest.

Risk: The local Docker service may be exposed beyond the intended local machine.

Mitigation: Bind the service to 127.0.0.1 only, add resource limits, control network exposure, and avoid uploading sensitive images unless the container publisher is trusted.

## Reference(s):

- [ClawHub BBDuck skill page](https://clawhub.ai/zhaoolee/skills/bbduck)
- [BBDuck local Swagger UI](http://127.0.0.1:28642/docs)
- [BBDuck local OpenAPI JSON](http://127.0.0.1:28642/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands, API request examples, JSON snippets, and concise result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include streaming log summaries with spend_time_ms and ZIP download instructions.]

## Skill Version(s):

0.2.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
