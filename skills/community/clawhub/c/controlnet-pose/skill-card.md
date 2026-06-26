## Description: <br>
Pose-conditioned image and video generation on RunComfy via the `runcomfy` CLI, routing between Kling Motion Control, Wan Animate, and Z-Image Turbo ControlNet LoRA based on the user's reference media and generation goal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to choose and invoke RunComfy routes for pose-conditioned image generation, video motion transfer, and related ControlNet workflows from explicit user-provided prompts and media URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RunComfy prompts, reference media URLs, and generated outputs may be processed by RunComfy and consume account quota or credits. <br>
Mitigation: Use only user-approved prompts and media URLs, keep the RunComfy token private, and confirm expected quota or credit use before running generation. <br>
Risk: Installing or invoking an unofficial CLI package could expose credentials or execute untrusted code. <br>
Mitigation: Install only the official RunComfy CLI package and restrict shell use to `runcomfy` commands needed for the requested workflow. <br>
Risk: Third-party reference media can influence generated outputs in ways that diverge from the user's prompt. <br>
Mitigation: Ingest only URLs the user explicitly provides and review generated media before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/controlnet-pose) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=controlnet-pose) <br>
- [Kling 2-6 Motion Control Pro](https://www.runcomfy.com/models/kling/kling-2-6/motion-control-pro?utm_source=clawhub&utm_medium=skill&utm_campaign=controlnet-pose) <br>
- [Wan 2-2 Animate video-to-video](https://www.runcomfy.com/models/community/wan-2-2-animate/video-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=controlnet-pose) <br>
- [Z-Image Turbo ControlNet LoRA](https://www.runcomfy.com/models/tongyi-mai/z-image/turbo/controlnet/lora?utm_source=clawhub&utm_medium=skill&utm_campaign=controlnet-pose) <br>
- [Mastering ControlNet in ComfyUI](https://www.runcomfy.com/tutorials/mastering-controlnet-in-comfyui?utm_source=clawhub&utm_medium=skill&utm_campaign=controlnet-pose) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline bash commands and JSON input snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the RunComfy CLI to save generated image or video outputs into a local output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
