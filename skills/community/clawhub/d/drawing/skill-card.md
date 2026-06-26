## Description: <br>
Generate children's drawings and coloring pages with modular prompts, style packs, and print-ready constraints across image models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn drawing, coloring-page, worksheet, or educational illustration requests into kid-safe, model-portable image prompts with clear style, age, and print constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt text or reference images may be sent to the selected image provider through the user's active image-generation workflow. <br>
Mitigation: Use trusted providers, avoid unnecessary personal details or identifiable child photos, and review prompts before generation. <br>
Risk: The skill can remember drawing preferences, age bands, style choices, and recurring prompt constraints under ~/drawing/. <br>
Mitigation: Review or clear ~/drawing/ to reset saved preferences, and tell the agent when preference memory should be paused or avoided. <br>


## Reference(s): <br>
- [Drawing on ClawHub](https://clawhub.ai/ivangdavila/drawing) <br>
- [Drawing homepage](https://clawic.com/skills/drawing) <br>
- [OpenAI image generation guide](https://platform.openai.com/docs/guides/image-generation) <br>
- [OpenAI GPT Image cookbook example](https://cookbook.openai.com/examples/generate_images_with_gpt_image) <br>
- [Google Vertex AI image prompt guide](https://cloud.google.com/vertex-ai/generative-ai/docs/image/image-prompts-design) <br>
- [OpenClaw models documentation](https://docs.openclaw.ai/concepts/models) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with reusable prompt templates, style guidance, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local preference notes under ~/drawing/ and produces provider-neutral prompt guidance unless the user asks for OpenClaw model configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
