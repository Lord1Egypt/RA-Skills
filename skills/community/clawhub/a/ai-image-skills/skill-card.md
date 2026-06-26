## Description: <br>
Build and execute skills.video image generation REST requests from OpenAPI specs. Use when user needs to create, debug, or document image generation calls on open.skills.video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuyun](https://clawhub.ai/user/chuyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to build, execute, debug, and document skills.video image generation requests from OpenAPI contracts, with SSE-first execution and polling fallback until terminal status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A helper can send SKILLS_VIDEO_API_KEY to an arbitrary URL if misused. <br>
Mitigation: Keep calls restricted to relative /generation/... paths or the official open.skills.video host, and avoid full URLs from untrusted prompts or documents. <br>
Risk: Using the skill can spend skills.video credits. <br>
Mitigation: Install and run it only when the user accepts SKILLS_VIDEO_API_KEY access and possible credit usage; stop retries for insufficient-credit errors until the user recharges. <br>


## Reference(s): <br>
- [Ai Image Skills on ClawHub](https://clawhub.ai/chuyun/ai-image-skills) <br>
- [skills.video Open Platform API Contract](references/open-platform-api.md) <br>
- [Image Model Endpoints Snapshot](references/image-model-endpoints.md) <br>
- [skills.video Open Platform API](https://open.skills.video/api/v1) <br>
- [skills.video Developer Dashboard](https://skills.video/dashboard/developer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns only terminal generation results and avoids reporting non-terminal IN_QUEUE or IN_PROGRESS states as final.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
