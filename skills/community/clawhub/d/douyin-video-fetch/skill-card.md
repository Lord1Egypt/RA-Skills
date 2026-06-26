## Description: <br>
Downloads Douyin videos to local MP4 files, preferring no-watermark sources and supporting URL, video_id, batch input, and a shared output directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KAMIENDER](https://clawhub.ai/user/KAMIENDER) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content analysts use this skill to download authorized Douyin videos as local MP4 inputs for later video analysis, recreation, or sample-library workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The downloader launches a headless browser and contacts Douyin or video-hosting endpoints. <br>
Mitigation: Run it only in environments where that network activity is allowed and use it only for videos you are authorized to download. <br>
Risk: The CLI reads a batch file path supplied by the user and writes MP4 files to the selected output directory. <br>
Mitigation: Use a dedicated output folder and avoid pointing --file at sensitive local files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/KAMIENDER/douyin-video-fetch) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, JSON, Text] <br>
**Output Format:** [MP4 files plus terminal status lines or JSON summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes video_id.mp4 files to the selected output directory; batch input can be read from a text file.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
