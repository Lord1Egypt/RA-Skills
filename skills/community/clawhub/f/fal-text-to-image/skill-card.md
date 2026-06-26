## Description: <br>
Generate, remix, and edit images using fal.ai's AI models. Supports text-to-image generation, image-to-image remixing, and targeted inpainting/editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[delorenj](https://clawhub.ai/user/delorenj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and external users use this skill to generate images from prompts, remix existing images, and perform targeted inpainting or object edits through fal.ai models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, source images, masks, or image URLs may be sent to fal.ai for remote image processing. <br>
Mitigation: Avoid confidential prompts, sensitive personal images, secrets, and internal-only image URLs unless that use is approved. <br>
Risk: fal.ai API use may incur costs under the user's API key. <br>
Mitigation: Monitor fal.ai usage and pricing before running large or high-resolution generation workflows. <br>
Risk: Generated images may retain embedded prompt, model, and parameter metadata. <br>
Mitigation: Strip EXIF metadata before publishing or sharing generated images when metadata disclosure is not intended. <br>


## Reference(s): <br>
- [fal.ai Documentation](https://docs.fal.ai/) <br>
- [fal.ai Model Playground](https://fal.ai/explore/search) <br>
- [fal.ai Pricing](https://fal.ai/pricing) <br>
- [fal.ai API Keys](https://fal.ai/dashboard/keys) <br>
- [Model Comparison](references/model-comparison.md) <br>
- [Usage Examples](references/usage-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline bash commands and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images may include prompt, model, and parameter metadata in EXIF.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
