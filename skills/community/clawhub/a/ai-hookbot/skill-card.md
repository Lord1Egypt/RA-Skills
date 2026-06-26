## Description: <br>
AI Hookbot helps an agent scrape YouTube Shorts hooks from a creator, trim them, and stitch them with a CTA video into ready-to-post vertical clips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jean-maradiaga](https://clawhub.ai/user/jean-maradiaga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators use this skill to run a local Hookbot pipeline that turns creator Shorts and a CTA video into short-form clips for TikTok, Reels, and Shorts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs separate Hookbot pipeline scripts that are not included in the artifact. <br>
Mitigation: Review the pipeline source before execution and set HOOKBOT_SCRIPTS_DIR only to a trusted local directory. <br>
Risk: Viral sorting may use a YouTube API key. <br>
Mitigation: Use the API key only when needed, keep it out of shared logs, and pass it through the documented environment variable. <br>
Risk: Raw failures may expose local paths or secret values. <br>
Mitigation: Sanitize error output before sharing logs or summaries. <br>


## Reference(s): <br>
- [ClawHub AI Hookbot release page](https://clawhub.ai/jean-maradiaga/ai-hookbot) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [FFmpeg](https://ffmpeg.org/) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, configuration guidance, and run summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying pipeline is expected to create 9:16 MP4 files and an output manifest.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
