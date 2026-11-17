## Description:

Runs lightweight Feishu/Lark group-chat English games across vocab, clue-guessing, and speaking modes with deterministic word scoring and SenseASR transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hei-maom](https://clawhub.ai/user/hei-maom)

### License/Terms of Use:

MIT-0

## Use Case:

External teams and chat-group facilitators use this skill to run English vocabulary, clue-guessing, and speaking-practice games in Feishu/Lark group chats. It helps the agent choose modes, maintain session state, score word guesses, transcribe selected voice messages, and provide concise learning feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Speaking mode sends selected voice-message audio to SenseASR for transcription.

Mitigation: Confirm the group is comfortable with external transcription before use and give an explicit notice before voice transcription is enabled.

Risk: A configurable ASR base URL could direct audio to an unintended service.

Mitigation: Keep SENSEAUDIO_BASE_URL unset or set only to a trusted HTTPS SenseASR endpoint.

Risk: ASR transcripts do not provide trustworthy phoneme-level pronunciation scoring.

Mitigation: Use transcripts for practical expression feedback only and avoid precise pronunciation grades or accent judgments without a dedicated pronunciation model.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hei-maom/skills/english-game)
- [SenseAudio API endpoint](https://api.senseaudio.cn)
- [SenseASR notes for speaking mode](references/asr_provider_notes.md)
- [Feishu English game integration guide](references/integration_cn.md)
- [Mode design](references/modes_cn.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Natural-language chat guidance with inline shell commands and plain-text helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Vocab scoring produces deterministic emoji score rows; speaking transcription returns transcript text for concise feedback.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
