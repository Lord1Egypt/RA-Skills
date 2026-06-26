## Description: <br>
Generate AI music videos end-to-end. Creates music with Suno (sunoapi.org), generates visuals with OpenAI/Seedream/Google/Seedance, and assembles into music video with ffmpeg. Supports timestamped lyrics (auto SRT), Suno native music video generation, slideshow/video/hybrid modes. Token-based cost tracking per generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gprecious](https://clawhub.ai/user/gprecious) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative users use this skill to plan lyrics-driven scenes, generate AI music and visuals through provider APIs, and assemble final music videos with local FFmpeg scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider API keys can spend credits when music, image, or video generation runs. <br>
Mitigation: Use --dry-run before generation, keep keys scoped, and review estimated costs before running paid workflows. <br>
Risk: The skill runs local shell and FFmpeg workflows over media files and paths. <br>
Mitigation: Run in a trusted workspace, review generated commands and inputs, and keep FFmpeg and shell dependencies patched. <br>
Risk: Custom SUNO_CALLBACK_URL endpoints may receive task metadata and audio URLs. <br>
Mitigation: Leave SUNO_CALLBACK_URL at the default no-op value unless you control and trust the HTTPS callback endpoint. <br>
Risk: The security guidance notes the assembly script may have a shell syntax issue before the full workflow runs. <br>
Mitigation: Run --dry-run and the included tests first, then fix or review assembly behavior before relying on full video assembly. <br>


## Reference(s): <br>
- [AI Music Video on ClawHub](https://clawhub.ai/gprecious/ai-music-video) <br>
- [SunoAPI Reference](artifact/references/sunoapi.md) <br>
- [Visual Providers Reference](artifact/references/visual-providers.md) <br>
- [SunoAPI base endpoint](https://api.sunoapi.org/api/v1) <br>
- [OpenAI images endpoint](https://api.openai.com/v1/images/generations) <br>
- [OpenAI videos endpoint](https://api.openai.com/v1/videos/generations) <br>
- [Together video endpoint](https://api.together.xyz/v2/videos) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands and generated media/configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce prompts.json, cost_estimate.json, visuals_meta.json, lyrics.srt, audio files, visual assets, and final MP4 videos through local scripts and provider APIs.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
