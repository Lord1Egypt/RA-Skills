## Description:

Builds and executes skills.video video generation REST requests from OpenAPI specs for creating, debugging, and documenting calls on open.skills.video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-video](https://clawhub.ai/user/skills-video)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect skills.video OpenAPI definitions, prepare valid video generation payloads, execute SSE-first generation requests, and poll until a terminal result is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A helper script can be invoked with URL options that may send SKILLS_VIDEO_API_KEY to a non-skills.video server.

Mitigation: Use only the default https://open.skills.video API base and relative API paths unless strict HTTPS and host allowlisting are added and reviewed.

Risk: Video generation calls require a bearer API key and may fail or expose credentials if the key is hardcoded or shared in files.

Mitigation: Provide SKILLS_VIDEO_API_KEY through the OpenClaw skill environment or shell environment, and do not store the key in prompts, payload files, or committed configuration.

Risk: Long-running generation workflows can return intermediate queue states or disconnect before a terminal result.

Mitigation: Keep SSE open when available, use polling only as fallback, and return results only after COMPLETED, SUCCEEDED, FAILED, or CANCELED terminal states.

## Reference(s):

- [ai-video ClawHub Release](https://clawhub.ai/skills-video/skills/gen-video)
- [skills-video Publisher Profile](https://clawhub.ai/user/skills-video)
- [skills.video Homepage](https://skills.video)
- [skills-video Repository](https://github.com/skills-video/skills)
- [skills.video Open Platform API Contract](references/open-platform-api.md)
- [Video Model Endpoints](references/video-model-endpoints.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request templates, terminal generation status summaries, and setup guidance for SKILLS_VIDEO_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
