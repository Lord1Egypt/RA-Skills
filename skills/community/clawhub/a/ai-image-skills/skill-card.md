## Description:

Builds and executes skills.video image generation REST requests from OpenAPI specs for creating, debugging, and documenting image model calls on open.skills.video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuyun](https://clawhub.ai/user/chuyun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect skills.video OpenAPI specs, build schema-conformant image generation payloads, execute SSE-first generation requests, and wait for terminal results with polling fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe endpoint options could send the user's skills.video API key to arbitrary URLs.

Mitigation: Use relative open.skills.video endpoints only, avoid arbitrary --base-url or full --sse-endpoint values, and rotate the API key if it may have been exposed.

Risk: The skill can trigger paid image generation with SKILLS_VIDEO_API_KEY.

Mitigation: Use the skill only with authorized paid-generation access, prefer a secrets manager or session-only environment variable for the key, and monitor credit use.

## Reference(s):

- [skills.video Open Platform API Contract](artifact/references/open-platform-api.md)
- [Image Model Endpoints Snapshot](artifact/references/image-model-endpoints.md)
- [ClawHub Skill Page](https://clawhub.ai/chuyun/skills/ai-image-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON terminal results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [SSE-first image generation flow with polling fallback until terminal status.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
