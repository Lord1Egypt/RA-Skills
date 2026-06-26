## Description: <br>
Build and execute skills.video video generation REST requests from OpenAPI specs for creating, debugging, or documenting calls on open.skills.video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skills-video](https://clawhub.ai/user/skills-video) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn skills.video OpenAPI definitions into working video generation requests, including payload templates, SSE execution, polling fallback, and runtime error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a configured skills.video API key and one helper can send that key to a user-supplied URL outside the intended provider. <br>
Mitigation: Use the default open.skills.video endpoints, avoid untrusted OpenAPI files or prompts that provide full URLs, keep the key in scoped skill configuration, and monitor credit usage. <br>


## Reference(s): <br>
- [skills.video](https://skills.video) <br>
- [skills-video repository](https://github.com/skills-video/skills) <br>
- [skills.video Open Platform API Contract](references/open-platform-api.md) <br>
- [Video Model Endpoints Snapshot](references/video-model-endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call skills.video APIs with SKILLS_VIDEO_API_KEY and waits for terminal generation status before returning results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
