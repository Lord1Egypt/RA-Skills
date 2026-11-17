## Description:

Download Video/Music from YouTube/Bilibili/X/etc.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqiao](https://clawhub.ai/user/guoqiao)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to have an agent download video or music from supported media URLs into local media folders for playback, media-server access, or optional sharing back through Telegram when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads media from supplied URLs into local folders, which can consume storage or place files where local media servers expose them on a LAN.

Mitigation: Use a dedicated output folder, monitor storage use, and review which local folders are shared by media-server software.

Risk: Optional cookies may be used for authenticated access, making configured cookie paths sensitive.

Mitigation: Avoid placing sensitive cookies at the documented default paths, or use a dedicated low-privilege cookies file only when needed.

Risk: When used from Telegram, audio files may be sent back through Telegram.

Mitigation: Confirm the chat context and file path before sending audio, and avoid uploading sensitive downloads.

Risk: The skill installs Python dependencies at runtime and does not pin every dependency version.

Mitigation: Run it in a controlled environment and prefer a release with pinned dependencies for higher-assurance deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoqiao/skills/dl)
- [ClawHub metadata homepage](https://clawhub.ai/guoqiao/dl)
- [Universal Media Server setup example](https://github.com/guoqiao/skills/blob/main/dl/ums/ums_install.sh)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; the script prints a local file or folder path and creates downloaded media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and Python 3.12 or newer; supports optional cookies, custom output directories, playlist downloads capped at 30 items, video downloads capped at 2000 MB, and audio downloads capped at 30 MB.]

## Skill Version(s):

0.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
