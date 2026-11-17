## Description:

Generate video, images, audio, and music using 40+ AI models via fal.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiweiyuan](https://clawhub.ai/user/jiweiyuan)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, developers, and agent users use this skill to generate or transform images, videos, speech, music, sound effects, and media utilities through fal.ai model endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local media and prompts to fal.ai endpoints.

Mitigation: Use a dedicated, revocable fal.ai API key and provide only media and prompts suitable for third-party cloud processing.

Risk: The helper can download generated media and write files to local paths.

Mitigation: Run it in a restricted workspace, keep outputs in a dedicated directory, and add path, file-type, size, endpoint, and URL allowlists before unattended use.

Risk: Dependency and endpoint behavior may change at execution time.

Mitigation: Pin dependencies and review endpoint parameters before production or automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiweiyuan/skills/corespeed-art)
- [Publisher profile](https://clawhub.ai/user/jiweiyuan)
- [uv installation reference](https://github.com/astral-sh/uv)
- [PEP 723 inline script metadata](https://peps.python.org/pep-0723/)
- [fal.ai API keys](https://fal.ai/dashboard/keys)
- [Beatoven Music Generation](references/beatoven-music.md)
- [BRIA RMBG 2.0](references/bria-rmbg.md)
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

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local media output paths after invoking fal.ai endpoints; generated media is saved to user-selected files.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
