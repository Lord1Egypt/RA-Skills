## Description:

Automates downloading YouTube audio, launching Doubao, playing audio, and capturing translations for full video subtitle extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banner90](https://clawhub.ai/user/banner90)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to run an OpenClaw workflow that downloads YouTube audio, opens Doubao, plays the audio, and captures translated subtitles or text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The registered tool points to an absolute host path outside the reviewed package, so the executable implementation is missing from the artifact.

Mitigation: Inspect and trust the external Python file before installation or execution.

Risk: The workflow downloads YouTube audio, opens Doubao, plays audio, and writes host files.

Mitigation: Confirm the user has appropriate rights for the source media and accepts the local file writes and GUI automation behavior.

Risk: Windows GUI automation can fail or behave unpredictably when the desktop is unavailable.

Mitigation: Run only with an active visible Windows desktop and verify output paths after completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/banner90/skills/banner-youtube-translate-workflow)

## Skill Output:

**Output Type(s):** [text, JSON, files]

**Output Format:** [JSON status object with local audio and translation file paths; saved translation text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a visible Windows desktop and host-accessible audio and translation directories.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
