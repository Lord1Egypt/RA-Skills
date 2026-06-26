## Description: <br>
Play ambient sounds for focus, relaxation, meditation, and sleep, including white noise, pink noise, brown noise, rain, singing bowl, binaural beats, and brain-wave tones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leyao1017](https://clawhub.ai/user/leyao1017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, office workers, students, and other users can use this skill to play local ambient audio for concentration, relaxation, meditation, or sleep. It is intended for machines with ffmpeg/ffplay installed and audible output available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill plays audible local audio and may be disruptive in shared or production environments. <br>
Mitigation: Install and run it only on machines where audio playback is expected and acceptable. <br>
Risk: The expected sample audio files may be missing from the artifact or local installation. <br>
Mitigation: Verify that the samples directory exists and contains the required audio files, or generate the missing samples before use. <br>
Risk: The stop behavior can force-kill matching ffplay processes rather than only its own tracked player. <br>
Mitigation: Use explicit playback and stop commands, and avoid running unrelated ffplay processes with matching command patterns during use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leyao1017/ambient-audio) <br>
- [Publisher Profile](https://clawhub.ai/user/leyao1017) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Audio playback] <br>
**Output Format:** [Markdown guidance with shell commands and local audio playback] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local ffplay playback with selectable sound modes, duration, and volume.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
