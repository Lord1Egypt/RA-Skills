## Description: <br>
Create a verbatim transcript for a YouTube URL using Google Gemini, with speaker labels and paragraph breaks and without time codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create a clean local transcript document from a YouTube URL when they need speaker-attributed transcript text without timestamps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the selected YouTube URL, and the video title when available, to Google/YouTube services using a Gemini API key. <br>
Mitigation: Use it only for video URLs where that external data flow is acceptable, and keep GEMINI_API_KEY scoped and protected. <br>
Risk: Generated transcripts are saved locally in the workspace by default. <br>
Mitigation: Avoid sensitive or private video URLs unless local persistence is acceptable, and choose an appropriate output path when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/odrobnik/gemini-yt-video-transcript) <br>
- [Publisher profile](https://clawhub.ai/user/odrobnik) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text transcript file with the video title followed by speaker-labeled transcript lines.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and GEMINI_API_KEY; saves generated transcripts locally by default.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
