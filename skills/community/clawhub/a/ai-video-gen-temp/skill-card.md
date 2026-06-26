## Description: <br>
End-to-end AI video generation for creating videos from text prompts using image generation, video synthesis, voice-over, and FFmpeg editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmyg11](https://clawhub.ai/user/mmyg11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to guide an agent through generating short videos from prompts, assembling image sequences into MP4 files, and adding voice-over with configured AI providers and FFmpeg. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, narration text, and generated media may be sent to configured third-party AI providers. <br>
Mitigation: Avoid sensitive content and review provider terms before use. <br>
Risk: Use of paid AI APIs can incur provider charges. <br>
Mitigation: Use limited API keys with spending controls and monitor provider usage. <br>
Risk: Generated media outputs and FFmpeg commands can overwrite local files when output paths collide. <br>
Mitigation: Run the skill in a dedicated working folder and choose output filenames that will not replace important files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mmyg11/ai-video-gen-temp) <br>
- [README.md](README.md) <br>
- [QUICK_START.md](QUICK_START.md) <br>
- [OpenAI platform](https://platform.openai.com) <br>
- [LumaAI](https://lumalabs.ai) <br>
- [Runway](https://runwayml.com) <br>
- [Replicate](https://replicate.com) <br>
- [ElevenLabs](https://elevenlabs.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local MP4, PNG, and MP3 artifacts through Python scripts and FFmpeg.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
