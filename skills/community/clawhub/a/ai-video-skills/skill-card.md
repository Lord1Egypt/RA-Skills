## Description: <br>
Build and execute skills.video video generation REST requests from OpenAPI specs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuyun](https://clawhub.ai/user/chuyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to construct, run, debug, and document skills.video video generation REST requests from OpenAPI specs, including SSE-first execution and polling fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A paid-service API key could be sent to an untrusted URL if a custom full endpoint or base URL is supplied. <br>
Mitigation: Use only trusted HTTPS skills.video hosts, avoid custom full URLs or untrusted base URLs, and confirm the model, prompt, and cost before starting generation jobs. <br>
Risk: Video generation requests may consume paid credits. <br>
Mitigation: Use a skills.video API key only when paid generation is intended, and stop retries when errors indicate insufficient credits until the account is recharged. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chuyun/ai-video-skills) <br>
- [skills.video Open Platform API Contract](artifact/references/open-platform-api.md) <br>
- [Video Model Endpoints Snapshot](artifact/references/video-model-endpoints.md) <br>
- [skills.video Open Platform API](https://open.skills.video/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API payload templates, terminal status summaries, and retry or error-handling guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
