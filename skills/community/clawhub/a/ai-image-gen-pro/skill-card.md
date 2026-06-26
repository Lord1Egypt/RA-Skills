## Description: <br>
Generate and edit AI images with FLUX, Gemini, Grok, Seedream, Reve, and other inference.sh models from the infsh CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingze00000](https://clawhub.ai/user/bingze00000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run inference.sh image models for AI art, product mockups, concept art, social media graphics, marketing visuals, illustrations, image editing, upscaling, and text rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote image services may receive prompts, input images, image URLs, and other submitted content. <br>
Mitigation: Avoid submitting confidential prompts, private images, or sensitive URLs unless sharing them with the remote model provider is intended. <br>
Risk: The skill depends on the inference.sh CLI and its login flow. <br>
Mitigation: Confirm the CLI install source is trusted and understand where infsh login stores credentials before use. <br>
Risk: Paid image models can incur usage costs. <br>
Mitigation: Check pricing before running paid models. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/bingze00000/ai-image-gen-pro) <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI Install Instructions](https://raw.githubusercontent.com/inference-sh/skills/refs/heads/main/cli-install.md) <br>
- [Running Apps](https://inference.sh/docs/apps/running) <br>
- [Image Generation Example](https://inference.sh/docs/examples/image-generation) <br>
- [Apps Overview](https://inference.sh/docs/apps/overview) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with bash command examples and JSON CLI inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the inference.sh CLI and login; generated images, provider behavior, and costs depend on the selected remote model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
