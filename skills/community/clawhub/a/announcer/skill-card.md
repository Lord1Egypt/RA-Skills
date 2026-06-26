## Description: <br>
Announce text throughout the house via AirPlay speakers using Airfoil + ElevenLabs TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to turn text into audible household announcements over configured AirPlay speakers. It is intended for macOS environments with Airfoil, ffmpeg, Python 3, an ElevenLabs API key, and the companion ElevenLabs skill installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated speech is sent to a cloud TTS provider and then played audibly through configured speakers, so announcements may expose sensitive or personal information. <br>
Mitigation: Use an ElevenLabs API key intended for this purpose, avoid announcing secrets or sensitive personal information, and review message text before broadcast. <br>
Risk: The skill controls Airfoil on macOS and can broadcast audio to selected AirPlay speakers. <br>
Mitigation: Review the speaker list and exclusions in the local configuration before use, and install only in environments where this speaker control is intended. <br>


## Reference(s): <br>
- [Announcer GitHub repository](https://github.com/odrobnik/announcer-skill) <br>
- [Airfoil](https://rogueamoeba.com/airfoil/) <br>
- [ElevenLabs](https://elevenlabs.io) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, audio playback] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces audible announcements through configured AirPlay speakers; requires macOS, Airfoil, ffmpeg, Python 3, ELEVENLABS_API_KEY, and the ElevenLabs skill.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
