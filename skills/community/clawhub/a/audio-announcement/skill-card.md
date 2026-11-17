## Description:

Audio Announcement lets an OpenClaw agent speak short, real-time status updates using text-to-speech across supported platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wililam](https://clawhub.ai/user/wililam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add audible progress, completion, receipt, and error announcements to OpenClaw workflows. It is most useful when users want status updates without continuously watching logs or terminal output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task text may be spoken aloud, sent to an online TTS provider, and cached as MP3 files.

Mitigation: Use short non-sensitive announcement text, prefer offline or local playback for private work, and clear or disable cached audio when needed.

Risk: The skill encourages persistent cross-session voice announcements through agent files, shell profiles, and heartbeat-style checks.

Mitigation: Install persistent hooks only with explicit approval, and avoid global profiles or agent identity files unless continuous announcements are intended.

Risk: Announcement scripts execute subprocesses and local audio players.

Mitigation: Review scripts and dependencies before deployment, and pass only trusted announcement strings to runtime commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wililam/skills/audio-announcement)
- [README](artifact/README.md)
- [Skill Documentation](artifact/SKILL.md)
- [Anti-Forgetting Mechanism](artifact/docs/announcement-anti-forgetting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance, Audio]

**Output Format:** [Markdown guidance with inline Python and shell examples; runtime commands generate short spoken audio announcements.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use online text-to-speech, local playback tools, and locally cached MP3 files depending on configuration.]

## Skill Version(s):

2.0.8 (source: server release evidence, package metadata, setup.py, and version.txt)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
