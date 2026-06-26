## Description: <br>
Use PotPlayer to play local or network audio/video files, with playback control, playlist management, seeking, fullscreen mode, subtitle loading, and device access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isaiah5818](https://clawhub.ai/user/isaiah5818) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to produce PotPlayer commands for opening local media, network streams, playlists, subtitles, and common playback controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce commands that open network media URLs, which may expose the user to untrusted media links. <br>
Mitigation: Require explicit user confirmation before opening network URLs and avoid untrusted media links. <br>
Risk: The skill documents webcam, screen capture, DVD, and device input commands that could access sensitive sources. <br>
Mitigation: Require explicit confirmation before webcam input, screen capture, DVD, or other device input is opened. <br>
Risk: The skill can open file, folder, or URL dialogs that may reveal private paths or prompt access to sensitive locations. <br>
Mitigation: Require explicit confirmation before opening file, folder, or URL dialogs and avoid use on screens showing private information. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/isaiah5818/ctrl-potplayer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume PotPlayer is installed on Windows at C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
