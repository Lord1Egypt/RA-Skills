## Description: <br>
Generate 4-second videos from text prompts and first and last frame images using the Head Tail to Video (Wan2.1) API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hy-1990](https://clawhub.ai/user/Hy-1990) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to configure and call a third-party video-generation workflow that turns a prompt plus first and last frame images into a short video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and first/last frame images are sent to the NewportAI/Dreamface third-party API. <br>
Mitigation: Use only with data approved for that provider, and avoid sensitive, personal, confidential, or regulated images and prompts unless the provider's privacy and retention practices are acceptable. <br>
Risk: The workflow requires an API key for the third-party service. <br>
Mitigation: Use a dedicated or revocable API key and rotate or revoke it if access is no longer needed. <br>


## Reference(s): <br>
- [NewportAI Head Tail to Video API](https://api.newportai.com/api-reference/head-tail-to-video-wan2-1) <br>
- [NewportAI Get Started](https://api.newportai.com/api-reference/get-started) <br>
- [Dreamface AI Tools](https://tools.dreamfaceapp.com/home) <br>
- [ClawHub Skill Page](https://clawhub.ai/Hy-1990/dream-head-tail-to-video) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and HTTP endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DREAMHEADTAILTOVIDEO_API_KEY and sends prompts plus image URLs or uploaded image assets to NewportAI/Dreamface.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
