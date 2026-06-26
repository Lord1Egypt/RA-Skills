## Description: <br>
Downloads a given video from YouTube, clips it from a specified start and end time, and saves the clip to a folder on the user's Desktop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bestisblessed](https://clawhub.ai/user/bestisblessed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create time-bounded MP4 clips from YouTube videos by providing a URL, start time, end time, and optional clip name. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads user-provided YouTube content and writes clips to ~/Desktop/Clips. <br>
Mitigation: Run it only for URLs the user intends to process and confirm the Desktop output location is appropriate for the environment. <br>
Risk: Using an existing clip name can overwrite a prior output file. <br>
Mitigation: Use unique clip names or check ~/Desktop/Clips before running the command. <br>
Risk: The full downloaded source video is deleted after clipping. <br>
Mitigation: Download or preserve the source separately when the original file must be retained. <br>


## Reference(s): <br>
- [Clip on ClawHub](https://clawhub.ai/bestisblessed/clip) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and MP4 file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates MP4 clips in ~/Desktop/Clips and requires yt-dlp and ffmpeg.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
