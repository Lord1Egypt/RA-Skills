## Description: <br>
Transform long videos into viral short-form clips with detected moments, captions, and exports for TikTok, Reels, and Shorts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mayank8290](https://clawhub.ai/user/Mayank8290) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, media teams, and developers use this skill to turn long-form videos or supported video URLs into short vertical clips with local transcription, heuristic moment selection, and styled captions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local media-processing binaries against user-supplied videos and supported URLs. <br>
Mitigation: Install trusted versions of ffmpeg, yt-dlp, and whisper-cpp, and review video sources before execution. <br>
Risk: Generated clips, transcripts, and summaries are saved locally under the OpenClaw videos output folder. <br>
Mitigation: Avoid confidential, regulated, or copyrighted videos unless local retention of transcripts and media artifacts is acceptable. <br>


## Reference(s): <br>
- [Clips Machine on ClawHub](https://clawhub.ai/Mayank8290/clips-machine) <br>
- [Project homepage](https://github.com/Mayank8290/openclaw-video-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Local media files, JSON transcript and moment metadata, Markdown summary, and console progress text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces transcript.json, viral_moments.json, clip MP4 files, and summary.md under the OpenClaw videos output folder.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
