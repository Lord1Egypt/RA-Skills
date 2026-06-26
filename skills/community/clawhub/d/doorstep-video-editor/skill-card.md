## Description: <br>
Video Editor - 视频剪辑 helps agents perform local video and audio editing tasks such as trimming, merging, adding text or subtitles, changing speed or size, extracting or replacing audio, and generating simple text-based videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncsimok](https://clawhub.ai/user/ncsimok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and developers can use this skill to prepare short-form videos and local media assets without external APIs. It is suited for workflows that need trimming, merging, captions, text overlays, background music, speed changes, resizing, or audio extraction and replacement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes derived video or audio files locally and may overwrite or create files at paths selected in commands. <br>
Mitigation: Review input and output filenames before running commands and keep backups of important media. <br>
Risk: User-supplied media may contain sensitive content that is copied into derived clips, audio exports, subtitles, or text-overlay outputs. <br>
Mitigation: Use the skill only with media you are comfortable processing locally and storing as derived files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ncsimok/doorstep-video-editor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results from local media-processing scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or modifies local media files at user-selected output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
