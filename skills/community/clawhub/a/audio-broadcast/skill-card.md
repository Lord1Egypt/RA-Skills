## Description: <br>
Audio Broadcast controls Xiaoboshu broadcast devices for audio playback, volume changes, scheduled tasks, file management, and text-to-speech announcements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oxiaom](https://clawhub.ai/user/oxiaom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and developers use this skill to manage Xiaoboshu audio broadcast systems, including checking device status, playing or stopping audio, adjusting volume, managing scheduled broadcasts, uploading audio, and sending text-to-speech messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships a populated config.json credential file. <br>
Mitigation: Delete the bundled config.json token before use and log in with credentials for the intended Xiaoboshu account. <br>
Risk: Device, schedule, file, and volume operations use plain HTTP and can affect broadcast equipment. <br>
Mitigation: Use only a trusted Xiaoboshu server on a trusted LAN/VPN or behind HTTPS, and avoid exposing the server to untrusted networks. <br>
Risk: Commands can broadcast to all devices, change volume broadly, delete files, and modify or delete scheduled tasks. <br>
Mitigation: Require explicit user confirmation for broad playback, volume changes, file deletion, task deletion, and scheduled-broadcast changes. <br>
Risk: TTS text and uploaded audio may contain sensitive information that is sent to services and broadcast devices. <br>
Mitigation: Review message content and target devices before upload or broadcast, and avoid sending sensitive audio or TTS text unless the deployment is approved for it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oxiaom/audio-broadcast) <br>
- [Xiaoboshu API Reference](references/api.md) <br>
- [Xiaoboshu Postman API Collection](references/postman2.1.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local configuration, cached TTS audio, and uploaded audio files when the user runs the bundled scripts.] <br>

## Skill Version(s): <br>
1.1.4 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
