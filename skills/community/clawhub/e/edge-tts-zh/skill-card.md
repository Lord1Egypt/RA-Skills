## Description: <br>
Chinese text-to-speech skill that uses the Microsoft Edge TTS engine to generate Chinese voice audio without an API key, with documented voice, speed, pitch, subtitle, and output options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hamlet0168](https://clawhub.ai/user/hamlet0168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to convert Chinese text into speech for messages, article reading, notifications, and podcast or video narration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes under-disclosed patching scripts that can silently modify installed skill files. <br>
Mitigation: Audit or remove artifact/scripts/patch.py and artifact/scripts/fix.py before deployment, and install only from reviewed release contents. <br>
Risk: Generated audio may play automatically instead of only being saved to a file. <br>
Mitigation: Run the skill in a controlled environment, confirm playback behavior before use, and disable or remove automatic playback if file-only output is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hamlet0168/edge-tts-zh) <br>
- [Publisher Profile](https://clawhub.ai/user/hamlet0168) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Audio files with command-line status text and output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text input with voice, rate, pitch, output path, file input, and format options documented by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
