## Description:

Send native voice bubbles via Feishu by converting text to OGG/Opus audio with edge-tts and ffmpeg, then sending it through the Feishu message tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxzcy](https://clawhub.ai/user/cxzcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn text replies into Feishu-native playable voice messages when a conversation calls for voice output or a voice response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can turn message text or options into shell command execution.

Mitigation: Patch the helper to use execFileSync or spawnSync with argument arrays and validate message text, voice, rate, and output path values before use.

Risk: Generated temporary audio files are written under /tmp and are not automatically cleaned up.

Mitigation: Delete temporary MP3 and OGG files after sending, and avoid placing sensitive message content in long-lived temporary files.

Risk: The conversion command can silently overwrite the selected output file.

Mitigation: Require explicit overwrite confirmation or generate unique output paths before running ffmpeg.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxzcy/skills/feishu-voice-bot)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and message tool call examples; the helper script outputs an OGG/Opus file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires edge-tts, ffmpeg, and a Feishu-capable message tool; temporary audio files are written under /tmp.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
