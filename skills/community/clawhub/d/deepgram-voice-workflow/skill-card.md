## Description:

Deepgram Voice Workflow supports an end-to-end Deepgram STT and TTS pipeline for transcribing voice messages, generating spoken replies, and building shell-based audio workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengbad](https://clawhub.ai/user/mengbad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to wire Deepgram speech-to-text and text-to-speech into shell-based bot, chat, and voice-message workflows. It is especially suited for lightweight Telegram, QQ, OneBot, and Chinese speech pipelines that need transcript files, raw API JSON, optional MP3 replies, and pipeline JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can fall back to a root-scoped credential file for DEEPGRAM_API_KEY.

Mitigation: Provide an explicit least-privilege DEEPGRAM_API_KEY in the runtime environment, avoid relying on /root/.openclaw/.env, and do not run the scripts as root.

Risk: Default output locations can write transcripts, raw API JSON, reply text, and generated speech to temporary or adjacent files.

Mitigation: Set private explicit output directories with restrictive permissions and remove local audio, transcript, JSON, and MP3 artifacts when no longer needed.

Risk: Input audio, reply text, transcripts, and generated speech may be sent to Deepgram or stored locally.

Mitigation: Use the workflow only with data approved for Deepgram processing and local storage under the deployment's privacy and retention requirements.

## Reference(s):

- [STT Notes](references/stt-notes.md)
- [TTS Notes](references/tts-notes.md)
- [Pipeline Notes](references/pipeline-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/mengbad/skills/deepgram-voice-workflow)

## Skill Output:

**Output Type(s):** [Text, JSON, Audio files, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with bash commands; scripts emit transcript text, raw API JSON, pipeline JSON, and MP3 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPGRAM_API_KEY; default STT language is zh and default TTS model is aura-2-luna-en.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
