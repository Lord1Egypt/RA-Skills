## Description: <br>
Call fal.ai model APIs for image generation (text-to-image and image-to-image). Use when a user asks to integrate fal, construct requests, run jobs, handle auth, or return image URLs from fal model APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xxmzdxxxm](https://clawhub.ai/user/xxmzdxxxm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to integrate fal.ai text-to-image and image-to-image model APIs, construct SDK or REST requests, handle authentication, and return generated image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: fal.ai API keys or other credentials could be exposed if hardcoded into generated examples or shared logs. <br>
Mitigation: Keep fal.ai API keys in environment variables and avoid embedding secrets directly in code or prompts. <br>
Risk: Prompts, source images, or generated outputs may be processed by fal.ai and should be treated as third-party API data. <br>
Mitigation: Confirm model inputs before submitting jobs and avoid sending prompts or images that should not be processed by fal.ai. <br>
Risk: Model schemas and response fields vary by fal.ai model and can change over time. <br>
Mitigation: Verify the selected model's current documentation before constructing requests or parsing image URLs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xxmzdxxxm/falimagegen) <br>
- [Fal Model API Checklist](references/fal-model-api-checklist.md) <br>
- [fal Model API Examples](references/fal-model-examples.md) <br>
- [fal model API quickstart](https://docs.fal.ai/model-apis/quickstart) <br>
- [Generate images from text](https://docs.fal.ai/model-apis/guides/generate-images-from-text) <br>
- [fal client documentation](https://docs.fal.ai/model-apis/client) <br>
- [fal model endpoints](https://docs.fal.ai/model-apis/model-endpoints) <br>
- [fal queue endpoints](https://docs.fal.ai/model-apis/model-endpoints/queue) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns implementation guidance and generated image URL handling patterns; no files are produced by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
