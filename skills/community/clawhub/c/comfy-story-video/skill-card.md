## Description: <br>
Generate illustrated children's story videos with ComfyUI images and local TTS narration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenlin0517](https://clawhub.ai/user/shenlin0517) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate children's story text, AI illustrations, narration, and draft video assets from a story theme using a local ComfyUI instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Theme or story text can be interpolated into local shell commands during TTS and FFmpeg steps. <br>
Mitigation: Use only trusted story inputs, run the skill in a limited local workspace, and prefer a patched version that uses subprocess.run argument lists and sanitized filename components. <br>
Risk: The workflow depends on a local ComfyUI service and writes generated media into the workspace. <br>
Mitigation: Keep ComfyUI bound to localhost and review generated JSON, images, audio, and video before reuse or publication. <br>


## Reference(s): <br>
- [Comfy Story Video on ClawHub](https://clawhub.ai/shenlin0517/comfy-story-video) <br>
- [ComfyUI children's story video generator reference](references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands; generated artifacts are JSON, PNG, MP3, and MP4 files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local ComfyUI at 127.0.0.1:8188, Python dependencies, FFmpeg, and macOS say for TTS.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
