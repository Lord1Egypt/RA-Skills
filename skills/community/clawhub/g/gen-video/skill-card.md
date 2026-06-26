## Description: <br>
Build and execute skills.video video generation REST requests from OpenAPI specs for creating, debugging, or documenting video generation calls on open.skills.video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skills-video](https://clawhub.ai/user/skills-video) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect skills.video OpenAPI contracts, construct valid video-generation payloads, execute SSE-first generation requests, and fall back to polling until a terminal result is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A helper can send the API key to an arbitrary URL if a full URL or untrusted endpoint is supplied. <br>
Mitigation: Restrict base URLs and endpoint overrides to documented open.skills.video paths and avoid untrusted OpenAPI specs or full URLs. <br>
Risk: Prompts, media references, and generated task data are sent to an external paid video-generation API. <br>
Mitigation: Do not submit sensitive, confidential, or proprietary content unless the user accepts the provider receiving that data. <br>
Risk: Generation may consume paid credits and can fail when credits are exhausted. <br>
Mitigation: Check billing or credits before retrying payment-related failures, and retry only after credits are recharged. <br>


## Reference(s): <br>
- [skills.video Open Platform API Contract](references/open-platform-api.md) <br>
- [Video Model Endpoints Snapshot](references/video-model-endpoints.md) <br>
- [skills.video](https://skills.video) <br>
- [skills-video skills repository](https://github.com/skills-video/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payload templates, shell commands, and terminal API result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SKILLS_VIDEO_API_KEY, prefers SSE results, and falls back to polling until COMPLETED, SUCCEEDED, FAILED, or CANCELED.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
