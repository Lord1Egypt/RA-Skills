## Description: <br>
Generate speech audio using ComfyUI Qwen-TTS service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YHSI5358](https://clawhub.ai/user/YHSI5358) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to convert text into speech audio through a configured ComfyUI Qwen-TTS service, with options for voice character, style, model size, output path, and sampling parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text is sent to the configured ComfyUI server for speech generation. <br>
Mitigation: Use only trusted ComfyUI hosts and avoid sending sensitive text to remote or shared servers. <br>
Risk: Weak validation of voice, style, model, and output parameters can lead to unexpected behavior or unsafe file paths. <br>
Mitigation: Keep character, style, and model values within documented choices and choose output paths that will not overwrite important files. <br>


## Reference(s): <br>
- [ComfyUI TTS ClawHub Page](https://clawhub.ai/YHSI5358/comfyui-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and option descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces speech audio through ComfyUI and returns or documents the generated output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
