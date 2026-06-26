## Description: <br>
A toolkit for local image and video processing plus Atlas Cloud image and video generation, covering upscaling, face enhancement, background removal, object erasing, face swapping, segmentation, media processing, and cloud generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihhhh](https://clawhub.ai/user/xixihhhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and media operators use this skill to generate, enhance, edit, and batch-process images or videos from an agent workflow. It supports local processing for common media tasks and Atlas Cloud API calls when cloud generation is requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: uv installs Python dependencies when tools are first run. <br>
Mitigation: Run the skill in a controlled environment and review dependency installation behavior before using it on production or sensitive systems. <br>
Risk: Local models can create large disk caches during first-run downloads. <br>
Mitigation: Confirm available disk space and cache locations before batch processing or first-time model use. <br>
Risk: Cloud generation sends prompts and reference images to Atlas Cloud. <br>
Mitigation: Use local tools for sensitive media and only send cloud prompts or images that are appropriate to share with the service. <br>
Risk: Atlas Cloud API credentials are required for cloud generation. <br>
Mitigation: Store the Atlas API key in environment variables or a protected .env file and do not paste it into prompts or generated outputs. <br>
Risk: Face-swap and NSFW-capable generation can be misused without consent or rights. <br>
Mitigation: Use these capabilities only with appropriate permission, rights, and policy review for the media involved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xixihhhh/free-image-and-video-generation) <br>
- [Publisher profile](https://clawhub.ai/user/xixihhhh) <br>
- [Atlas Cloud](https://www.atlascloud.ai?utm_source=github&utm_campaign=free-image-and-video-generation-skill) <br>
- [uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated media files saved to local output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are saved under ./output/ by default unless an explicit output path is supplied.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
