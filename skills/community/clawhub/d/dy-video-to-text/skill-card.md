## Description: <br>
Extracts speech-to-text from Douyin videos, parses video metadata, and downloads watermark-free videos from Douyin share links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hljwwyy123](https://clawhub.ai/user/hljwwyy123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process Douyin share links, retrieve video metadata or local video files, and transcribe video speech through Alibaba Cloud ASR when an API key is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Douyin links are sent to Douyin/ByteDance for link resolution, and video URLs may be sent to Alibaba Cloud for transcription. <br>
Mitigation: Install only when that network sharing is acceptable, and avoid pasting unrelated private URLs or sensitive text around the Douyin link. <br>
Risk: Text extraction requires DASHSCOPE_API_KEY and may incur Alibaba Cloud ASR usage costs. <br>
Mitigation: Store the key with the OpenClaw secrets mechanism, monitor API usage, and parse links before transcribing batches to avoid wasted calls. <br>
Risk: Dependency installation uses Python package managers and downloaded videos are written to local storage. <br>
Mitigation: Prefer a virtual environment for dependencies and choose an appropriate output directory for downloaded video files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hljwwyy123/dy-video-to-text) <br>
- [Alibaba Cloud Bailian API key setup](https://help.aliyun.com/zh/model-studio/get-api-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save downloaded MP4 files to a user-specified local directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
