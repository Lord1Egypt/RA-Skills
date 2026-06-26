## Description: <br>
Use when someone asks for Flux image generation, Flux text-to-image prompts, Flux image model selection, or CLI-based image generation with Flux-style models on ricebowl.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinchanzis](https://clawhub.ai/user/jinchanzis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to configure the ai-media CLI, select a Flux-capable image model, generate images from prompts, and retrieve generated image tasks through ricebowl.ai. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys can be exposed through configuration commands or shared terminal output. <br>
Mitigation: Use a dedicated, revocable API key and avoid sharing output from commands that may display configured credentials. <br>
Risk: Image generation requests may spend paid credits or target an unintended service endpoint. <br>
Mitigation: Confirm the configured base URL, selected model, and expected credit exposure before running generation commands. <br>


## Reference(s): <br>
- [ai-media-generator homepage](https://github.com/214140846/ai-media-generator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model-listing commands, image-generation commands, image retrieval commands, and cautions for API key and base URL handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
