## Description: <br>
Download videos, audio, subtitles, and covers from Bilibili using bilibili-api. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BenAngel65](https://clawhub.ai/user/BenAngel65) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operators use this skill to download Bilibili videos, audio, subtitles, covers, and playlists with configurable quality and cookie-based access where required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bilibili session cookies can grant account access if exposed. <br>
Mitigation: Treat BILIBILI_SESSDATA like a password and do not paste it into chats, logs, screenshots, shared shells, or committed files. <br>
Risk: Download scripts can write media and subtitle files to local paths. <br>
Mitigation: Use a normal downloads folder and review the configured output directory before running scripts. <br>
Risk: Running downloader scripts with elevated privileges can increase the impact of mistakes. <br>
Mitigation: Do not run the scripts as administrator or root. <br>


## Reference(s): <br>
- [Quick Guide](references/quick_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code examples plus JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local media, subtitle, cover, and configuration files in user-selected download directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
