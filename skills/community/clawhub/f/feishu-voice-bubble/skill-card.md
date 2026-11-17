## Description:

Send native Feishu/Lark voice bubble messages by converting text to Opus audio with Microsoft Edge TTS and preparing the resulting audio for Feishu chat delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saokiritokun](https://clawhub.ai/user/saokiritokun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create Feishu/Lark voice-bubble replies from text, including longer messages split at sentence boundaries and optional voice, rate, and pitch controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for speech generation is sent to Microsoft Edge TTS.

Mitigation: Avoid sensitive or regulated content unless the workflow is approved for that external service.

Risk: The helper requires installing the node-edge-tts npm dependency.

Mitigation: Pin and review the npm dependency before installation or deployment.

Risk: Generated audio is written to user-provided output paths.

Mitigation: Keep generated audio paths inside a dedicated output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saokiritokun/skills/feishu-voice-bubble)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands and JSON status output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces .opus audio files for Feishu audio messages; long text may produce numbered output files.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
