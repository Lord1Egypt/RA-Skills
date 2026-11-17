## Description:

Checks and prepares videos for platform-specific cross-posting, then posts or schedules them through WoopSocial after the user approves a plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and social media teams use an AI agent to check a finished video against platform requirements, prepare platform-specific captions and settings, and review one posting plan. The agent can then post or schedule through WoopSocial after approval, or provide pages for manual posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags that an API key in an MCP URL could be exposed through saved configuration or logs.

Mitigation: Review the API-key setup instructions and avoid placing a key in a URL that may be saved or logged.

## Reference(s):

- [Job file format](references/job-file.md)
- [Platform requirements](references/platforms.md)
- [Caption writing guidance](references/writing.md)
- [WoopSocial setup and usage](references/woopsocial.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML, JSON, Shell commands]

**Output Format:** [Markdown and HTML plan pages, JSON job and request files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific text and account settings for one video or a batch.]

## Skill Version(s):

1.0.0 (source: target metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
