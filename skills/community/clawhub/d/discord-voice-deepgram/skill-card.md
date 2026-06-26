## Description: <br>
Voice-channel conversations in Discord using Deepgram streaming STT and low-latency TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adriel1006](https://clawhub.ai/user/adriel1006) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to let an OpenClaw or Clawdbot agent join Discord voice channels, transcribe permitted speakers through Deepgram, route speech to the agent, and play concise spoken responses back into the channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spoken Discord input can reach the agent's normal toolset. <br>
Mitigation: Use a restricted tool profile or separate approval before enabling voice-triggered access to powerful tools. <br>
Risk: Voice audio is sent to Deepgram and transcripts may be logged. <br>
Mitigation: Install only in controlled Discord servers and inform channel participants before use. <br>
Risk: The bot may listen to unintended speakers if broad speaker permissions or auto-join are enabled. <br>
Mitigation: Configure numeric Discord IDs for primaryUser or allowedUsers and keep autoJoinChannel disabled unless it is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adriel1006/discord-voice-deepgram) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/adriel1006) <br>
- [Deepgram Listen API endpoint](https://api.deepgram.com/v1/listen) <br>
- [Deepgram Speak API endpoint](https://api.deepgram.com/v1/speak) <br>


## Skill Output: <br>
**Output Type(s):** [text, audio, shell commands, configuration, guidance] <br>
**Output Format:** [Spoken Discord audio plus JSON/text tool responses and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Discord and Deepgram credentials; streams Discord voice audio to Deepgram for speech-to-text and text-to-speech.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
