## Description: <br>
Download videos from YouTube and other video platforms. Use when user needs to download videos for offline viewing, extract audio from videos, or save video metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to download videos for offline viewing, extract audio, choose video quality or format, and inspect video metadata when they have rights to the content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install an unpinned yt-dlp package before running. <br>
Mitigation: Install and pin yt-dlp in a controlled virtual environment before using the skill. <br>
Risk: Downloading media can create legal, storage, and content-handling risk. <br>
Mitigation: Review the URL, output path, file type, disk space, and rights to the content before running downloads. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text, Guidance] <br>
**Output Format:** [Python command-line invocation, stdout text, and local media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads video or audio files to a local output path and can print available formats or metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
