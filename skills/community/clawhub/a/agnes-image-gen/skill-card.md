## Description: <br>
Uses Agnes AI image-generation models to create images from text prompts and edit existing images, with guidance for custom API keys, prompt quality, natural-looking outputs, and clearer Chinese text rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuwu2495](https://clawhub.ai/user/jiuwu2495) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users use this skill to generate or edit images through Agnes AI models, including text-to-image prompts, image-to-image edits, style changes, and Chinese text layout refinement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles reusable API keys and may expose credentials if users paste keys into chat. <br>
Mitigation: Prefer setting AGNES_API_KEY through the environment and avoid sharing long-lived keys directly in prompts. <br>
Risk: Prompts and input images are sent to Agnes AI for generation or editing. <br>
Mitigation: Avoid confidential images, proprietary prompts, personal data, or material that should not be processed by a third-party image service. <br>
Risk: The documented one-command wrapper script is referenced, but the artifact evidence contains only SKILL.md. <br>
Mitigation: Verify the wrapper script is present and reviewed before relying on the documented automated workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiuwu2495/agnes-image-gen) <br>
- [Agnes AI](https://agnes-ai.com) <br>
- [Agnes image generations API](https://apihub.agnes-ai.com/v1/images/generations) <br>
- [Agnes image edits API](https://apihub.agnes-ai.com/v1/images/edits) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated image files or image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require an AGNES_API_KEY and may send prompts or images to Agnes AI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
