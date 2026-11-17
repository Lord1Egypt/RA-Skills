## Description:

Play audio files using Windows media player with non-blocking execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banner90](https://clawhub.ai/user/banner90)

### License/Terms of Use:

MIT

## Use Case:

Developers and workflow authors use Audio Play to trigger non-blocking playback of local audio files in a Windows media player, including as a step in a YouTube translation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package does not include the Python implementation that the plugin entry would execute, and the entry points to an external absolute path.

Mitigation: Review the external audio_play.py path on the target machine or require a package-relative bundled implementation before installation.

Risk: Windows GUI automation depends on a visible desktop session.

Mitigation: Run only in environments where an interactive Windows desktop is available and document expectations for disconnected sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/banner90/skills/audio-play)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON status object for tool results, with Markdown usage documentation in the skill source]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-blocking playback; requires local Windows media player configuration and a visible desktop for GUI automation.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact package.json and openclaw.plugin.json list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
