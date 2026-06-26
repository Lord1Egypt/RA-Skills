## Description: <br>
Downloads Douyin videos from shared links and returns video metadata with the saved local file path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andjie98](https://clawhub.ai/user/andjie98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to parse Douyin share links, download a video to the OpenClaw workspace, and receive basic metadata such as title, author, engagement counts, file path, and file size. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads media from a user-provided URL and writes it to the local OpenClaw workspace. <br>
Mitigation: Run it only with trusted Douyin share links and review the downloaded file before reuse or redistribution. <br>
Risk: Each new download deletes the previous douyin_last.mp4 file. <br>
Mitigation: Copy any video that must be retained before running another download. <br>
Risk: Security confidence is limited by the available evidence even though the recorded verdict is clean. <br>
Mitigation: Review the skill text before installing and avoid granting credentials, broad write access, or external-action authority unless a deployment requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andjie98/douyin-video) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/andjie98) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, files] <br>
**Output Format:** [Console text followed by a JSON result and a downloaded MP4 file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node; writes a single fixed file at ~/.openclaw/workspace/douyin-downloads/douyin_last.mp4 and replaces the previous download.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
