## Description: <br>
Generates 4-second videos from text descriptions and images using the DreamAPI/NewportAI Image to Video (Wan2.1) API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hy-1990](https://clawhub.ai/user/Hy-1990) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and creators use this skill to configure an API key and generate short videos from a prompt plus an image URL or uploaded local image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and uploaded local images are sent to external DreamAPI/NewportAI services. <br>
Mitigation: Avoid sensitive, private, regulated, or confidential images unless the provider's data handling terms have been reviewed. <br>
Risk: The skill requires a DreamAPI/NewportAI API key. <br>
Mitigation: Store the key in DREAMIMAGETOVIDEO_API_KEY through OpenClaw configuration and do not paste real credentials into prompts or shared files. <br>


## Reference(s): <br>
- [DreamAPI get started](https://api.newportai.com/api-reference/get-started) <br>
- [Image to Video Wan2.1 API reference](https://api.newportai.com/api-reference/image-to-video-wan2-1) <br>
- [Dreamface AI tools](https://tools.dreamfaceapp.com/home) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and HTTP endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DREAMIMAGETOVIDEO_API_KEY; prompt input is limited to 1500 characters, with optional 480p or 720p resolution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
