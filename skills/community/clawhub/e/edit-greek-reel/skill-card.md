## Description: <br>
Edit a raw talking-head video into a polished short-form reel with Greek karaoke subtitles. Trims silence, adds Manrope Bold subtitles, zoom effects, SFX, and image overlays. Usage - /edit-greek-reel <path-to-video> [options] <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[artemisln](https://clawhub.ai/user/artemisln) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media editors, and Claude Code users use this skill to turn raw Greek talking-head footage into short vertical reels with subtitles, trims, zooms, sound effects, and overlays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs local ffmpeg and Python tools against user video files. <br>
Mitigation: Install dependencies in a virtual environment and review commands and local file paths before execution. <br>
Risk: Generated transcripts, temporary files, and output videos may contain private speech or sensitive media. <br>
Mitigation: Review video and transcript sensitivity before use, and delete transcript.json and temporary files when they are no longer needed. <br>


## Reference(s): <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [Manrope font](https://fonts.google.com/specimen/Manrope) <br>
- [ClawHub skill page](https://clawhub.ai/artemisln/edit-greek-reel) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown instructions with shell and Python snippets; the workflow writes transcript JSON, temporary media files, and a final MP4 video.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local ffmpeg, Python, Whisper, Pillow, and optional image or audio assets supplied near the input video.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
