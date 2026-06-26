## Description: <br>
Downloads and monitors Bilibili favorite folders with incremental checks, MP4 merging, and optional Telegram notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[name8266](https://clawhub.ai/user/name8266) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure authenticated Bilibili favorite-folder downloads, run one-time or scheduled checks, and receive optional Telegram notifications when new videos are downloaded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cookie guide contains a credential-handling mismatch by directing users toward Douyin cookies instead of cookies for the intended Bilibili domain. <br>
Mitigation: Only export cookies for the exact Bilibili domain being used, keep cookie files private with restrictive permissions, and avoid sharing cookies in chat or logs. <br>
Risk: The setup flow may install packages or downloaded binaries system-wide. <br>
Mitigation: Review the setup script before running sudo or installing downloaded binaries, and prefer trusted package-manager or pinned installation paths where possible. <br>


## Reference(s): <br>
- [Bilibili Fav Downloader on ClawHub](https://clawhub.ai/name8266/bilibili-fav-downloader) <br>
- [Bilibili Cookie Guide](references/cookie-guide.md) <br>
- [Bilibili Favorite ID Guide](references/favorite-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and Python or shell script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime downloader can create MP4 files, logs, and state files in user-configured output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
