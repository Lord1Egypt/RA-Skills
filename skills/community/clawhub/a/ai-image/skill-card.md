## Description: <br>
Build and execute skills.video image generation REST requests from OpenAPI specs for creating, debugging, or documenting image generation calls on open.skills.video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skills-video](https://clawhub.ai/user/skills-video) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure skills.video API access, inspect OpenAPI contracts, build valid image-generation payloads, execute SSE-first generation requests, and fall back to polling until a terminal result is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured API key may be sent to caller-supplied URLs outside the intended skills.video service. <br>
Mitigation: Use the default https://open.skills.video API base, avoid custom full URLs or base URLs unless verified as controlled by skills.video, and prefer a version that allowlists the intended API host before adding Authorization headers. <br>
Risk: The skill requires a bearer API key for runtime API calls. <br>
Mitigation: Store SKILLS_VIDEO_API_KEY in the agent or shell environment, keep it out of files and prompts, and rotate it if it may have been exposed. <br>


## Reference(s): <br>
- [AI Image ClawHub Skill Page](https://clawhub.ai/skills-video/ai-image) <br>
- [skills.video Homepage](https://skills.video) <br>
- [skills-video Skills Repository](https://github.com/skills-video/skills) <br>
- [skills.video Open Platform API Contract](references/open-platform-api.md) <br>
- [Image Model Endpoints Snapshot](references/image-model-endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses API-key-backed calls to skills.video, prefers SSE results, and should return only terminal generation states.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
