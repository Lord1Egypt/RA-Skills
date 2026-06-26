## Description: <br>
Play audio files using Windows media player with non-blocking execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banner90](https://clawhub.ai/user/banner90) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation users use this skill to launch local audio playback as part of a Windows and WSL-based YouTube translation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package points to an absolute local Python entry file that is not included in the release, so the executable behavior cannot be fully reviewed from the artifact. <br>
Mitigation: Install only after independently inspecting and trusting the configured local audio_play.py file and any media player configuration it uses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/banner90/audio-play) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON status objects with command and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success status, audio path, selected player, duration, or error fields.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
