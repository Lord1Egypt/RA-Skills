## Description: <br>
Searches Bilibili videos, generates or runs yt-dlp download commands, and retrieves video metadata, comments, danmaku, and creator video lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[epantrip](https://clawhub.ai/user/epantrip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Bilibili, inspect video details, prepare downloads, and retrieve comments or danmaku while managing local dependencies such as yt-dlp and ffmpeg. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some scripts may run unintended local code or make system/account-affecting changes without enough user control. <br>
Mitigation: Review scripts before installing, avoid administrator or root execution, and run them from a dedicated low-privilege download directory. <br>
Risk: Comment and UP-video-list scripts accept inputs that security guidance says should not be trusted until input handling is fixed. <br>
Mitigation: Do not run those scripts with untrusted or nonnumeric arguments. <br>
Risk: Cookie files may grant access to a Bilibili account. <br>
Mitigation: Treat cookies.txt like a password file and keep it out of shared directories and logs. <br>
Risk: Automatic dependency installation can alter the local Python environment. <br>
Mitigation: Install yt-dlp manually in a trusted environment and review dependency versions before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/epantrip/bilibili-video-downloader) <br>
- [README](artifact/README.md) <br>
- [Installation Guide](artifact/INSTALL.md) <br>
- [Permissions and Safety Notes](artifact/PERMISSIONS.md) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>
- [BBDown Releases](https://github.com/nilaoda/BBDown/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files, Text] <br>
**Output Format:** [Markdown with inline shell commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local video files, XML danmaku files, comment text, JSON-derived metadata, and dependency checks when scripts are executed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
