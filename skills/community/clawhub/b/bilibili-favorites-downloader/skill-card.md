## Description: <br>
Downloads videos from a user's Bilibili favorites, with pagination, size filtering, list-only export, and batch downloading through yt-dlp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hhjin](https://clawhub.ai/user/hhjin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to back up, review, or download publicly accessible Bilibili favorites for offline use. It can also list favorites without downloading videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may download many videos and use substantial bandwidth and disk space. <br>
Mitigation: Start with list-only mode, then use a small maximum download count, an explicit output folder, and a size limit before larger runs. <br>
Risk: Users may be tempted to provide account secrets while preparing a Bilibili favorites URL. <br>
Mitigation: Provide only the Bilibili favorites URL or ID; do not provide cookies, passwords, or account tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hhjin/bilibili-favorites-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create MP4 video files locally and print download or list-only summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
