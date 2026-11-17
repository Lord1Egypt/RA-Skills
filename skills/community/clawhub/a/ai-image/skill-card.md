## Description:

Build and execute skills.video image generation REST requests from OpenAPI specs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-video](https://clawhub.ai/user/skills-video)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to create, debug, or document image generation requests against the skills.video Open Platform API. It helps inspect OpenAPI schemas, produce endpoint-ready payloads, execute SSE-first generation calls, and wait for terminal results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the user's API key to an unintended network destination if endpoint options are misused.

Mitigation: Use it only with the intended https://open.skills.video API, avoid full custom URLs or untrusted base URLs, and review endpoint arguments before execution.

Risk: API keys may be exposed if users hardcode SKILLS_VIDEO_API_KEY in files or shell profile snippets.

Mitigation: Store SKILLS_VIDEO_API_KEY in managed skill environment settings and avoid committing credentials to files.

Risk: The security verdict is suspicious, so installation may carry higher review requirements.

Mitigation: Review the skill before installing and scan changes before deployment.

## Reference(s):

- [skills.video homepage](https://skills.video)
- [skills-video repository](https://github.com/skills-video/skills)
- [Open Platform API Contract](references/open-platform-api.md)
- [Image Model Endpoints](references/image-model-endpoints.md)
- [AI Image ClawHub listing](https://clawhub.ai/skills-video/skills/ai-image)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads, shell commands, and JSON event output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLS_VIDEO_API_KEY for live API calls; helpers use SSE first and polling only as fallback until terminal generation status.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
