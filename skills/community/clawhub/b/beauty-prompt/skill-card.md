## Description: <br>
Interior design image helper that turns home renovation, spatial design, and commercial display requests into refined prompts and generated visual concepts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[865116251](https://clawhub.ai/user/865116251) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to refine interior design, furnishing, spatial layout, and commercial display ideas into image-generation prompts, review the Chinese and English prompt text, generate an image, and optionally request a video handoff from the generated image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Design prompts can expose private addresses, client-confidential layouts, personal identifiers, or sensitive business details through web search, image generation, delivery, or handoff. <br>
Mitigation: Avoid including sensitive personal, client, location, or business information in prompts or generated-image workflows. <br>
Risk: Generated images are saved in the workspace output directory and may be sent through Feishu. <br>
Mitigation: Review generated images and file paths before sharing, and manage retained output files according to the workspace's data-handling policy. <br>
Risk: Optional video creation shares the generated image path with another agent after a positive user response. <br>
Mitigation: Only approve the video handoff when the generated image and local path are appropriate to share with that agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/865116251/beauty-prompt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown conversation text with Chinese and English prompt text, shell command examples, generated image file paths, and optional video handoff guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved under the workspace output directory and may be delivered through Feishu; optional video creation shares the generated image path with another agent after user approval.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and server-provided changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
