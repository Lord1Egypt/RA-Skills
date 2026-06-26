## Description: <br>
Downloads a public Douyin video without a watermark from a user-provided link, saves it locally, uploads it to cloud storage, and returns a share link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexliu9921](https://clawhub.ai/user/alexliu9921) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn a Douyin video link into a locally downloaded MP4 and a temporary cloud share link for saving or sharing permitted media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save and share copies of Douyin videos. <br>
Mitigation: Use it only for media the user has permission to download, save, and share. <br>
Risk: Downloaded files are written under /tmp and uploaded to a cloud link with temporary retention. <br>
Mitigation: Clean up local files and shared cloud copies when the content should no longer be accessible. <br>
Risk: The workflow depends on a user-provided media URL and remote video availability. <br>
Mitigation: Confirm the link is the intended public Douyin video before running the download and upload steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexliu9921/alexliutkdownload) <br>
- [Publisher profile](https://clawhub.ai/user/alexliu9921) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text and Markdown guidance with shell commands, a local MP4 path, and a cloud share link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates /tmp/douyin_<video_id>.mp4 and returns a cloud link that the skill notes is retained for about 30 days.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
