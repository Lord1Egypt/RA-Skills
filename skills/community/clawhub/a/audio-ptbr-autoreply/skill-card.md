## Description: <br>
Brazilian Portuguese voice reply helpers for OpenClaw that transcribe audio locally with wav2vec2, generate a short agent reply locally by default or with Anthropic when configured, and synthesize a local Piper voice response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henrique-simoes](https://clawhub.ai/user/henrique-simoes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add a Brazilian Portuguese voice loop to OpenClaw, especially for mobile, accessibility, Telegram-style, and hands-busy workflows. It processes an audio file into a transcript, asks the agent for a short response, and returns a synthesized voice reply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The published /voz trigger is malformed and may expose shell-command injection depending on how OpenClaw expands command arguments. <br>
Mitigation: Fix the trigger to pass structured argv values or apply robust escaping before enabling it in environments where other users can send /voz commands. <br>
Risk: Transcript text can be sent to Anthropic when ANTHROPIC_API_KEY is configured. <br>
Mitigation: Leave ANTHROPIC_API_KEY unset when transcript text must remain local, and document this privacy boundary for operators. <br>
Risk: The skill runs the Piper binary from the configured WORKSPACE path. <br>
Mitigation: Use only a trusted WORKSPACE and verify installed Piper assets before deployment. <br>
Risk: The optional local audio hook example uses shell-expanded template values and is unsafe for untrusted inputs. <br>
Mitigation: Do not publish or enable the hook unless the platform passes structured arguments or the local operator has reviewed and accepted the risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/henrique-simoes/audio-ptbr-autoreply) <br>
- [Server-resolved publisher profile](https://clawhub.ai/user/henrique-simoes) <br>
- [wav2vec2 Portuguese ASR model](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-portuguese) <br>
- [Piper PT-BR voice models](https://huggingface.co/rhasspy/piper-voices) <br>
- [Piper release assets](https://github.com/rhasspy/piper/releases/tag/v1.2.0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Plain text command output, voice-selection messages, and a MEDIA directive that references a generated OGG audio file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The main processing flow reads one audio file, emits a transcript-derived response, and writes temporary audio output; optional Anthropic mode sends transcript text only when ANTHROPIC_API_KEY is set.] <br>

## Skill Version(s): <br>
2.1.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
