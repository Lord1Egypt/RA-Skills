## Description: <br>
Generate video, images, audio, and music using 40+ AI models via fal.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiweiyuan](https://clawhub.ai/user/jiweiyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to generate or transform media with fal.ai-hosted image, video, audio, music, upscaling, background-removal, and lip-sync models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a fal.ai API key and can spend fal.ai credits when generation jobs are submitted. <br>
Mitigation: Use a revocable API key, monitor fal.ai usage, and run only generation requests the user has approved. <br>
Risk: Prompts, URLs, images, videos, or audio selected for a job are sent to fal.ai or upstream model providers for processing. <br>
Mitigation: Avoid sensitive or regulated media unless external processing is acceptable for the user's use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiweiyuan/corespeed-art) <br>
- [fal.ai API keys](https://fal.ai/dashboard/keys) <br>
- [PEP 723 inline script metadata](https://peps.python.org/pep-0723/) <br>
- [uv](https://github.com/astral-sh/uv) <br>
- [Beatoven Music Generation](references/beatoven-music.md) <br>
- [BRIA RMBG 2.0](references/bria-rmbg.md) <br>
- [FLUX](references/flux.md) <br>
- [GPT Image 1.5](references/gpt.md) <br>
- [Kling Video](references/kling.md) <br>
- [LTX 2.3](references/ltx.md) <br>
- [MiniMax Speech-02 HD](references/minimax-speech.md) <br>
- [Nano Banana](references/nanobanana.md) <br>
- [Pixverse Video](references/pixverse.md) <br>
- [Qwen Image](references/qwen.md) <br>
- [Recraft V4](references/recraft.md) <br>
- [Seedream](references/seedream.md) <br>
- [Sora 2](references/sora.md) <br>
- [Sync Lipsync 2.0](references/sync-lipsync.md) <br>
- [Topaz Upscale](references/topaz.md) <br>
- [Veo 3.1](references/veo.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media files are saved locally by the bundled fal.ai helper script when the agent runs it.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
