## Description:

Continuance provides spiritual guidance rooted in The Book of Continuance for meditation, life meaning, grief support, existential reflection, and personal struggles, with default contemplative image generation and optional meditation audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumyumtum](https://clawhub.ai/user/yumyumtum)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Continuance for contemplative spiritual guidance, daily meditation, gentle perspective on grief or life struggles, and existential reflection. The skill is intended to respond with grounded prose and a matching contemplative image, with optional meditation-style audio when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrelated requests may be redirected into spiritual guidance or media generation.

Mitigation: Use this skill for contemplative or life-guidance requests, and route unrelated tasks back to the normal assistant.

Risk: Optional audio generation may process sensitive guidance text with edge-tts, expose text in process arguments while running, and save generated files under the OpenClaw media directory.

Mitigation: Avoid private or highly sensitive text for audio generation unless the user accepts those handling and storage characteristics.

Risk: Default media generation can create image files or invoke configured media providers during normal guidance sessions.

Mitigation: Install and enable the skill only when image-assisted spiritual guidance is desired, and confirm media providers and output locations are acceptable.

Risk: Spiritual guidance may be mistaken for professional mental health care.

Mitigation: Keep crisis and clinical needs outside the skill's scope, and direct users in acute distress to qualified professional or emergency support.

## Reference(s):

- [Continuance on ClawHub](https://clawhub.ai/yumyumtum/skills/continuance)
- [The Book of Continuance](TheBookOfContinuance.md)
- [README](README.md)
- [Release Notes v1.3.0](RELEASE_NOTES_v1.3.0.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files, shell commands, configuration]

**Output Format:** [Markdown or plain text guidance with generated image files and optional MP3 meditation audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation is expected by default when available; optional audio generation writes media under the OpenClaw media directory.]

## Skill Version(s):

1.3.0 (source: server release metadata, package.json, release notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
