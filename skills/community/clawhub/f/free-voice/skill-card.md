## Description:

Generate Russian male voice audio using ComfyUI with the Qwen3 TTS node and save it as an MP3 voice message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onimka](https://clawhub.ai/user/onimka)

### License/Terms of Use:


## Use Case:

Developers and ComfyUI users use this skill to generate Russian male voice audio from text through a local ComfyUI workflow and deliver the resulting MP3 as a voice message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends prompt text to a local ComfyUI API and writes generated audio to a configured Windows output folder.

Mitigation: Use it only with the intended local ComfyUI setup, and review or change the endpoint and output path before running in a different environment.

Risk: The artifact assumes a Russian male voice configuration and specific ComfyUI node, model, and file paths.

Mitigation: Confirm the required ComfyUI plugin, Qwen3 model, language, and save directory are installed and appropriate for the target use case.

## Reference(s):

- [Free voice from Comfy UI + Qwen3 TTS](https://clawhub.ai/onimka/skills/free-voice)
- [Publisher profile: onimka](https://clawhub.ai/user/onimka)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local ComfyUI requests and saves generated MP3 audio to the configured output folder.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
