## Description: <br>
Generate children's drawings and coloring pages with modular prompts, style packs, and print-ready constraints across image models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[12357851](https://clawhub.ai/user/12357851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn requests for children's drawings, printable coloring pages, and simple educational illustrations into age-appropriate, model-portable image prompts and refinement guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt text and optional reference images may be sent to the selected image provider. <br>
Mitigation: Use trusted providers, avoid identifiable child photos and unnecessary personal details, and review prompts before generation. <br>
Risk: The skill may keep drawing-related preferences and prompt patterns in ~/drawing/ or workspace memory. <br>
Mitigation: Install only when local preference memory is acceptable and review or remove stored preferences when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/12357851/drawing-bak) <br>
- [Skill homepage](https://clawic.com/skills/drawing) <br>
- [OpenAI image generation guide](https://platform.openai.com/docs/guides/image-generation) <br>
- [OpenAI image generation cookbook](https://cookbook.openai.com/examples/generate_images_with_gpt_image) <br>
- [Google Vertex AI image prompt guide](https://cloud.google.com/vertex-ai/generative-ai/docs/image/image-prompts-design) <br>
- [OpenClaw models documentation](https://docs.openclaw.ai/concepts/models) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with natural-language image prompts, prompt templates, refinement guidance, and occasional shell command blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May advise local preference files under ~/drawing/ and prompts or reference images for a user-selected image provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
