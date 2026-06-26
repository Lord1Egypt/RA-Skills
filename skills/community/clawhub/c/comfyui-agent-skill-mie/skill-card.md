## Description: <br>
Agent skill for running registered ComfyUI workflows through a stable CLI, supporting image, video, music, and speech generation on a local or trusted self-hosted ComfyUI server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miemieeeee](https://clawhub.ai/user/miemieeeee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check ComfyUI availability and run registered local or trusted self-hosted workflows for image generation, image editing, video, music/audio, and speech synthesis with structured JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded images, prompts, generated media, saved server URLs, and async job records may contain private local data. <br>
Mitigation: Use only a local or trusted self-hosted ComfyUI server, avoid public or untrusted endpoints, and treat the tool's results directory as private data. <br>
Risk: Dependency behavior may vary across environments if installs are not pinned. <br>
Mitigation: Use a locked dependency install for sensitive environments and review dependency updates before deployment. <br>
Risk: Unreviewed ComfyUI workflows can change execution behavior or required models and nodes. <br>
Mitigation: Run registered workflows only, review analyzer-generated workflow configs before activation, and use doctor or preflight checks before long generation jobs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/miemieeeee/comfyui-agent-skill-mie) <br>
- [Skill instructions](SKILL.md) <br>
- [Workflow reference](references/workflows.md) <br>
- [CLI contract](references/cli.md) <br>
- [Workflow node requirements](references/workflow_nodes.md) <br>
- [Prompt enhancement: reference to image](references/prompt_enhancement/reference_to_image.md) <br>
- [Prompt enhancement: image to image](references/prompt_enhancement/image_to_image.md) <br>
- [Prompt enhancement: text to speech](references/prompt_enhancement/text_to_speech.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown instructions with CLI commands and structured JSON results; generated media is returned through local file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a reachable local or trusted self-hosted ComfyUI server and registered workflows; generated outputs may include PNG, MP4, or MP3 files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
