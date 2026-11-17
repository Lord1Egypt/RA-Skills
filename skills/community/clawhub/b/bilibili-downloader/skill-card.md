## Description:

Downloads Bilibili videos, audio, subtitles, danmaku, and covers using bilibili-api with quality and configuration options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benangel65](https://clawhub.ai/user/benangel65)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to prepare commands, scripts, and configuration for downloading Bilibili videos, playlists, audio, subtitles, covers, and related metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses live Bilibili session-cookie authentication.

Mitigation: Treat SESSDATA as a secret and keep it out of source files, tracked config, shared terminals, and logs.

Risk: The skill installs bilibili-api-python without a pinned or reviewed version.

Mitigation: Run the scripts in a virtual environment and pin or review dependency versions before use.

Risk: The skill downloads third-party media content.

Mitigation: Use it only for content you are authorized to access and download, and review Bilibili account and content terms before running downloads.

## Reference(s):

- [Bilibili API Quick Guide](references/quick_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/benangel65/skills/bilibili-downloader)
- [Publisher Profile](https://clawhub.ai/user/benangel65)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets plus JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include runnable scripts and configuration templates; downloaded media files are produced by executing the scripts outside the skill card.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
