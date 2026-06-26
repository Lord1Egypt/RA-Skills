## Description: <br>
Download Bilibili AI-generated subtitles (auto-subtitles) for videos. Use when you need to quickly get subtitles from Bilibili videos that have AI-generated captions. Supports 9 languages: Chinese, English, Japanese, Spanish, Arabic, Portuguese, Korean, German, French. Language priority can be customized. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[54Lynnn](https://clawhub.ai/user/54Lynnn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to download available Bilibili AI-generated captions for a video and produce a local transcript file with video information, a short summary preview, and full subtitle text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically use local Bilibili browser login cookies through yt-dlp when a supported browser profile is found. <br>
Mitigation: Run it without browser cookies for public videos when possible, or use a separate browser profile or account for member-only access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/54Lynnn/bilibili-ai-subtitle) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown context for a shell-script skill that produces a UTF-8 text transcript file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The transcript file includes video metadata, a summary preview, and full subtitle text when Bilibili AI subtitles are available.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
