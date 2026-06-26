## Description: <br>
Generate or edit images using Google's Nano Banana image models for explicit Gemini or Nano Banana requests, iterative edits, and reference-image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyagil](https://clawhub.ai/user/dyagil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route image-generation or image-editing requests to a local Nano Banana CLI backed by Gemini image models. It is intended for prompt-based image creation, multi-image reference edits, model selection, and delivery of generated image file paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an unbundled local CLI that can process the Gemini API key, prompts, and reference images outside the reviewed package. <br>
Mitigation: Review and independently trust the local nano-banana CLI before installation or execution. <br>
Risk: Gemini API credentials are required for normal use. <br>
Mitigation: Use a dedicated, restricted Gemini API key, store it with locked-down file permissions, and never log or paste it into chat. <br>
Risk: Prompts and reference images may be sent to Google and processed by the local helper script. <br>
Mitigation: Avoid private, regulated, or proprietary images unless the user accepts that data-sharing posture. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dyagil/dyagil-nano-banana) <br>
- [Google AI Studio API key setup](https://aistudio.google.com/apikey) <br>
- [Gemini generateContent API endpoint](https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a MEDIA path or platform attachment convention for generated image outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
