## Description:

A reusable Feishu voice loop: accept text or voice input, generate natural OpenAI speech, and deliver it to chat or web playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengzhuowen](https://clawhub.ai/user/pengzhuowen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow builders use this skill to add a reusable text-or-voice input loop that transcribes local audio when needed, generates OpenAI TTS audio, and delivers audio replies through Feishu or web playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message text, generated audio, Feishu recipient IDs, and Feishu app authentication material are sent to the intended OpenAI and Feishu services.

Mitigation: Use the skill only with content approved for those services, review Feishu app permissions, and avoid sensitive audio or business content unless policy allows it.

Risk: Local transcription relies on the audio command configured in ~/.openclaw/openclaw.json.

Mitigation: Review the configured transcription command before use and keep it limited to trusted local audio tooling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pengzhuowen/skills/feishu-voice-loop)
- [Input / Output Workflow](references/input-output-workflow.md)
- [Feishu Voice Loop Presets](references/presets.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate temporary audio files during TTS conversion; the --keep option prints retained file paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
