## Description: <br>
Generate 4-second videos from text prompts using Text to Video (Wan2.1) through the Dream/Newport API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hy-1990](https://clawhub.ai/user/Hy-1990) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to turn short text prompts into 4-second videos through the Dream/Newport Text to Video API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt text and generated-video requests are sent to the external Dream/Newport API provider. <br>
Mitigation: Use the skill only when that provider is trusted, and avoid submitting confidential prompt text unless provider processing is acceptable. <br>
Risk: The skill requires an API key that could incur quota or billing impact if overused or exposed. <br>
Mitigation: Use a dedicated or limited API key where possible and monitor usage, quota, and billing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Hy-1990/dream-text-to-video) <br>
- [Dreamface AI tools homepage](https://tools.dreamfaceapp.com/home) <br>
- [Newport AI Text to Video Wan2.1 API reference](https://api.newportai.com/api-reference/text-to-video-wan2-1) <br>
- [Newport AI get started](https://api.newportai.com/api-reference/get-started) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and API endpoint details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DREAMTEXTTOVIDEO_API_KEY; prompts are documented with a 1500-character maximum and optional 480p or 720p resolution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
