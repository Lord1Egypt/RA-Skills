## Description:

ComfyUI绘画专业版 helps agents guide professional local AI image generation with ComfyUI, including automatic parameter tuning, CivitAI model management, image-to-image, ControlNet, and batch workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, design teams, and developers use this skill to operate local ComfyUI image-generation workflows for illustration, ecommerce imagery, game art, architecture visualization, and branded visual production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to run ComfyUI-related scripts, read selected input images, write model files, and contact CivitAI.

Mitigation: Install only for workflows where those actions are intended, and review agent file and network permissions before use.

Risk: Remote ComfyUI endpoints can expose image-generation workflows and local resources if misconfigured.

Mitigation: Keep the ComfyUI URL on localhost unless a trusted HTTPS remote setup is required and has been reviewed.

Risk: Downloaded AI models are third-party artifacts with their own quality, licensing, and safety properties.

Mitigation: Download models only from trusted sources and confirm their license and suitability before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/comfyui-painter-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [CivitAI API](https://civitai.com/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python code examples, configuration notes, and workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ComfyUI workflow guidance, prompt settings, model-management steps, and generated file paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
