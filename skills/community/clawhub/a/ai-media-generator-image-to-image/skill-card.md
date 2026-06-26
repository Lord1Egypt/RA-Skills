## Description: <br>
Use when someone asks for image-to-image, reference-image generation, transform image with prompt, edit image with AI, or CLI-based image-to-image workflows on ricebowl.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinchanzis](https://clawhub.ai/user/jinchanzis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to run AI image-to-image workflows with the ai-media CLI, including selecting a model, preparing a reference image, submitting an edit prompt, and retrieving the generated image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed through configuration output, terminal sharing, screenshots, logs, or chat transcripts. <br>
Mitigation: Confirm that `ai-media config show` masks keys before sharing output, and prefer environment variables or a secret manager for `AI_MEDIA_API_KEY`. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinchanzis/ai-media-generator-image-to-image) <br>
- [ai-media-generator homepage](https://github.com/214140846/ai-media-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AI_MEDIA_API_KEY and AI_MEDIA_BASE_URL; output may include CLI JSON from model listing commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
