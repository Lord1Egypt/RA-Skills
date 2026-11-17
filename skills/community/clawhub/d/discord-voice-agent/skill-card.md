## Description:

Helps build, configure, run, debug, and extend a Discord voice agent integrated with OpenClaw for setup, voice capture, transcription, TTS, slash commands, reply routing, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsvips](https://clawhub.ai/user/itsvips)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Discord server operators use this skill to set up and operate an OpenClaw-powered voice bot that joins a voice channel, captures speech, routes replies through OpenClaw, and speaks back with short responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discord and OpenClaw tokens could be exposed if pasted into shared chats or committed to source control.

Mitigation: Store tokens only in a secure environment or secret store, and avoid including them in chat transcripts, logs, or commits.

Risk: Voice turns, transcripts, and conversation history can contain sensitive participant data.

Mitigation: Make participants aware that the bot can capture, transcribe, and locally save voice turns and conversation history, and review retention practices before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itsvips/skills/discord-voice-agent)
- [Quickstart](references/quickstart.md)
- [Discord Voice Agent commands and knobs](references/commands.md)
- [Model routing](references/model-routing.md)
- [Model settings](references/model-settings.md)
- [One-command test mode](references/test-mode.md)
- [Discord Voice Agent troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local voice captures, JSONL history, and status output when troubleshooting.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
