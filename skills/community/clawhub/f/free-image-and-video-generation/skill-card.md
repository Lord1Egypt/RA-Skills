## Description:

Free local AI image and video processing toolkit with cloud AI generation for upscaling, face enhancement, background removal, object erasing, face swapping, segmentation, media processing, and Atlas Cloud image or video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihhhh](https://clawhub.ai/user/xixihhhh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to enhance, edit, convert, and generate image or video assets through local media tools and Atlas Cloud generation models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud generation can send prompts and reference images to Atlas Cloud.

Mitigation: Avoid private or sensitive media unless the provider and data handling terms are acceptable for the use case.

Risk: First use can download packages and model files into local caches.

Mitigation: Review dependencies before installation and run the skill in an isolated environment when handling untrusted media.

Risk: Face-swap and NSFW features can be misused without consent or policy controls.

Mitigation: Use these features only with clear authorization and apply additional review for identity, consent, and acceptable-use requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixihhhh/skills/free-image-and-video-generation)
- [uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/)
- [Atlas Cloud](https://www.atlascloud.ai?utm_source=github&utm_campaign=free-image-and-video-generation-skill)
- [Atlas Cloud model API](https://api.atlascloud.ai/api/v1/model)
- [InsightFace inswapper model artifact](https://huggingface.co/deepinsight/inswapper/resolve/main/inswapper_128.onnx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, file paths, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves generated or processed media files to ./output/ by default unless a custom output path is supplied.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
