## Description:

Generate video, images, audio, and music using 40+ AI models via fal.ai for media creation, editing, upscaling, background removal, lipsync, voiceover, and sound workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zypher-agent](https://clawhub.ai/user/zypher-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to route AI media requests to fal.ai models and save generated videos, images, audio, music, or utility outputs as files. It supports multi-model workflows for creation, editing, upscaling, background removal, lipsync, and voiceover generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fal.ai API key is exposed to the runtime that executes the skill.

Mitigation: Use a dedicated fal.ai API key with appropriate billing controls and revoke or rotate it after use when needed.

Risk: Prompts and uploaded media are sent to fal.ai endpoints.

Mitigation: Avoid sensitive prompts or private media unless sending them to fal.ai is intended and approved for the use case.

Risk: The helper can call unbounded endpoints and download remote output to arbitrary writable paths.

Mitigation: Review endpoints before execution, use a dedicated output directory, and constrain filenames to that directory.

Risk: Runtime dependencies are installed dynamically through uv.

Mitigation: Review and pin or lock runtime dependencies before deployment in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zypher-agent/skills/corespeed-studio)
- [fal.ai API keys](https://fal.ai/dashboard/keys)
- [uv package manager](https://github.com/astral-sh/uv)
- [PEP 723 inline script metadata](https://peps.python.org/pep-0723/)
- [Beatoven Music Generation](references/beatoven-music.md)
- [Background Removal - BRIA RMBG 2.0](references/bria-rmbg.md)
- [FLUX](references/flux.md)
- [GPT Image 1.5](references/gpt.md)
- [Kling Video](references/kling.md)
- [LTX 2.3](references/ltx.md)
- [MiniMax Speech-02 HD](references/minimax-speech.md)
- [Nano Banana](references/nanobanana.md)
- [Pixverse v5](references/pixverse.md)
- [Qwen Image 2 Pro](references/qwen.md)
- [Recraft V4 Pro](references/recraft.md)
- [Seedream](references/seedream.md)
- [Sora 2](references/sora.md)
- [Lipsync v2](references/sync-lipsync.md)
- [Topaz Upscale](references/topaz.md)
- [Veo 3.1](references/veo.md)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and saved media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and FAL_KEY; generated media is downloaded to requested output filenames.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
