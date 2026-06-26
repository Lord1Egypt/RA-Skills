## Description: <br>
Download Video/Music from YouTube/Bilibili/X/etc. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqiao](https://clawhub.ai/user/guoqiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to download user-requested video or audio from supported media URLs into local media folders for playback or library management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches media from user-provided URLs through yt-dlp and writes downloaded files to local folders, which can consume disk space and depend on third-party downloader behavior. <br>
Mitigation: Use it only for user-requested media, review the printed output path, and monitor the configured media directories for unexpected size growth. <br>
Risk: Configured cookie files can enable authenticated media access. <br>
Mitigation: Keep cookie files private, scope them to the intended services, and remove or rotate them when they are no longer needed. <br>
Risk: When used from Telegram, downloaded audio may be sent back to the chat. <br>
Mitigation: Confirm the Telegram context and the selected audio file before sending it to the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoqiao/dl) <br>
- [Universal Media Server setup example](https://github.com/guoqiao/skills/blob/main/dl/ums/ums_install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and script stdout path text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads media files to local output directories and may provide an audio file through Telegram when used in that channel.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
