## Description: <br>
End-to-end AI video generation from text prompts using image generation, video synthesis, voice-over, and FFmpeg editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rhanbourinajd](https://clawhub.ai/user/rhanbourinajd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content creators use this skill to generate short AI-assisted videos from prompts, convert image sequences to MP4, and add narrated voice-over to existing video files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider API keys and submitted prompts or media may be sent to external AI services. <br>
Mitigation: Use limited-scope API keys, keep secrets private, and avoid confidential prompts, scripts, images, audio, or video unless the providers' terms and retention policies are acceptable. <br>
Risk: Video generation and text-to-speech calls can create unexpected provider costs. <br>
Mitigation: Monitor API usage, prefer budget modes when testing, and verify provider pricing before batch or long-running generation. <br>
Risk: FFmpeg commands use overwrite behavior for selected outputs. <br>
Mitigation: Choose output paths carefully and avoid pointing commands at files that should be preserved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rhanbourinajd/ai-video-gen) <br>
- [OpenAI platform](https://platform.openai.com) <br>
- [LumaAI](https://lumalabs.ai) <br>
- [Runway](https://runwayml.com) <br>
- [ElevenLabs](https://elevenlabs.io) <br>
- [Replicate](https://replicate.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or modifies local MP4, PNG, and MP3 files when the bundled scripts are run with configured provider API keys and FFmpeg.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
