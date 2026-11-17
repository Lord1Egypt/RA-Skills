## Description:

Announce text throughout the house via AirPlay speakers using Airfoil + ElevenLabs TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:


## Use Case:

Developers and advanced home automation users use Announcer to generate ElevenLabs text-to-speech announcements and route them over AirPlay speakers with Airfoil on macOS. The skill supports configured speaker groups, targeted speaker announcements, optional chimes, and speaker status listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A tampered announcer configuration can create local code-execution risk through an AppleScript value.

Mitigation: Use the skill only with a trusted announcer config directory and review configuration changes before running announcements.

Risk: The ANNOUNCER_WORKSPACE value and sibling elevenlabs skill influence what configuration and text-to-speech code the script uses.

Mitigation: Run the skill only in a trusted workspace with the expected sibling elevenlabs skill installed.

Risk: Announcement text is sent to ElevenLabs for text-to-speech processing.

Mitigation: Do not announce sensitive text unless external processing by ElevenLabs is acceptable.

Risk: Invalid Airfoil volume configuration can affect speaker behavior.

Mitigation: Keep airfoil.volume configured as a numeric value between 0.0 and 1.0.

## Reference(s):

- [Announcer ClawHub skill page](https://clawhub.ai/odrobnik/skills/announcer)
- [Announcer setup instructions](SETUP.md)
- [Airfoil](https://rogueamoeba.com/airfoil/)
- [ElevenLabs](https://elevenlabs.io)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, JSON, Audio]

**Output Format:** [CLI commands, status text, optional JSON speaker listings, and generated speech audio routed through Airfoil]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, Airfoil, Python 3, ffmpeg, an ElevenLabs API key, and a sibling elevenlabs skill.]

## Skill Version(s):

1.2.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
