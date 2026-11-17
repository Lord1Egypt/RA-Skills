## Description:

Helps agents generate and edit Midjourney images and videos through Ace Data Cloud, then retrieve the results of submitted tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to request image or video generation and edits, describe images, and check the status of submitted tasks without repeating generation requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A service API key grants access to external API actions.

Mitigation: Confirm the publisher is @acedatacloud, use a separate key when possible, and restrict allowed API routes to required actions.

Risk: Prompts or uploaded images are processed externally and generation actions may incur charges.

Mitigation: Review the data before submission, check pricing and balance, and poll the original task ID rather than repeating a billable generation request.

## Reference(s):

- [Midjourney imagine API documentation](https://platform.acedata.cloud/documents/midjourney-imagine)
- [Midjourney task API documentation](https://platform.acedata.cloud/documents/midjourney-tasks)
- [Ace Data Cloud token setup and troubleshooting](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/authentication.md)
- [Midjourney MCP server documentation](https://github.com/AceDataCloud/MidjourneyMCP)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with API request examples and task-result guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation returns a task ID; a successful task may provide an image URL or raw image URL.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
