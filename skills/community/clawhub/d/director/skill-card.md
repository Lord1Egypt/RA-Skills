## Description: <br>
End-to-end pipeline for creating faceless Islamic story videos for TikTok, Reels, and Shorts by coordinating story research, scripting, image generation, voice narration, and video assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohamedzeidan2021](https://clawhub.ai/user/mohamedzeidan2021) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, content teams, and agent developers use this skill to generate short-form Islamic educational videos with faceless visuals, narrated scripts, subtitles, thumbnails, and publishing metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on web research, media-generation APIs, TTS providers, FFmpeg, and local output folders. <br>
Mitigation: Grant only scoped tool and filesystem access, configure provider API keys with limits, and review outputs before publishing. <br>
Risk: The stated faceless-content safety gate is not fully implemented in the included orchestrator. <br>
Mitigation: Implement and test face detection before relying on the skill to enforce faceless imagery for religiously sensitive subjects. <br>
Risk: Religious stories and citations may be incorrect or culturally inappropriate if generated without review. <br>
Mitigation: Review Quran, hadith, honorifics, and visual depictions with qualified human oversight before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mohamedzeidan2021/director) <br>
- [Publisher profile](https://clawhub.ai/user/mohamedzeidan2021) <br>
- [Visual Style Guide](artifact/visual_style_guide.md) <br>
- [Global Config](artifact/global_config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON schemas, Python orchestration code, shell command examples, and media file path conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed to produce story JSON, scene scripts, image and audio file paths, final MP4 videos, thumbnails, subtitles, logs, and publishing metadata when connected to the required external tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
