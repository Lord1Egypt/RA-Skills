## Description:

Generate images and videos through AI-video-agent. Supports image create, image remix, video create, and video animate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toolok5](https://clawhub.ai/user/toolok5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Canvas Claw to submit image and video generation tasks to a configured AI-video-agent service, including text-to-image, image remix, text-to-video, and image-to-video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, media, and authentication tokens to a configured AI-video-agent endpoint.

Mitigation: Use only trusted HTTPS endpoints or a strictly local localhost service approved for the data being processed.

Risk: Login flows can expose passwords or returned tokens when secrets are entered on the command line or printed in terminal output.

Mitigation: Avoid real passwords in command-line arguments, protect printed tokens, and prefer pre-provisioned environment variables for sensitive credentials.

Risk: Sensitive prompts or media may be submitted to a remote service that is not approved for that content.

Mitigation: Review the configured endpoint and data handling policy before submitting confidential prompts, images, or videos.

## Reference(s):

- [Canvas Claw on ClawHub](https://clawhub.ai/toolok5/skills/canvas-claw)
- [Installation Guide](INSTALL.md)
- [Canvas Claw Design](docs/plans/2026-04-07-canvas-claw-design.md)
- [Canvas Claw OpenClaw Skill Implementation Plan](docs/plans/2026-04-07-canvas-claw-openclaw-skill-plan.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and generated media output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AI_VIDEO_AGENT_BASE_URL, AI_VIDEO_AGENT_TOKEN, and AI_VIDEO_AGENT_SITE_ID environment variables.]

## Skill Version(s):

0.1.0 (source: release evidence and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
