## Description:

Plays algorithmically generated ambient sounds such as white, pink, and brown noise, rain, brain-wave tones, singing bowl, and binaural beats for focus, relaxation, meditation, or sleep.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leyao1017](https://clawhub.ai/user/leyao1017)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to ask an agent to start, stop, or list ambient audio modes for focus, relaxation, meditation, and sleep on a Linux machine with audio output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Duration and volume arguments are not bounded by the script before use.

Mitigation: Validate duration and volume as bounded numeric values before playback.

Risk: The script stores PID state in a shared temporary path and uses broad process matching to stop playback.

Mitigation: Use a private runtime directory for PID state and stop only the exact child process started by the skill.

Risk: The skill can play sound immediately and its setup guidance may require installing ffmpeg with sudo.

Mitigation: Confirm ffmpeg installation is acceptable for the environment and start playback at low volume.

## Reference(s):

- [Ambient Audio on ClawHub](https://clawhub.ai/leyao1017/skills/ambient-audio)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start local audio playback through ffplay and uses mode, duration, volume, stop, and list arguments.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
