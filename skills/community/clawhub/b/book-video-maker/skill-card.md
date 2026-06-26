## Description: <br>
Generates 1080x1920 vertical book-summary videos with AI images, text-to-speech narration, Ken Burns motion, and aligned subtitles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianzhufangna](https://clawhub.ai/user/jianzhufangna) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and marketing teams use this skill to turn book titles, authors, and quote JSON files into short vertical videos with generated illustrations, Chinese voiceover, subtitles, and final MP4 output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically installs Python dependencies during execution. <br>
Mitigation: Run it in a virtual environment and install trusted pinned dependency versions before use. <br>
Risk: The skill uses sensitive ARK/Doubao API credentials and searches additional local paths for API keys. <br>
Mitigation: Use a dedicated low-privilege API key, prefer environment-variable configuration, and avoid storing credentials in broadly readable local files. <br>
Risk: Book text, quote prompts, and generation prompts are sent to external AI and TTS services. <br>
Mitigation: Avoid private notes, unpublished manuscripts, sensitive quote text, or confidential prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jianzhufangna/book-video-maker) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown usage guidance, shell commands, JSON quote templates, and generated MP4 media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8 or newer, ffmpeg, and an ARK/Doubao API key; writes generated assets and final video files under the selected output directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata, skill.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
