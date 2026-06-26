## Description: <br>
Make AI phone calls using ElevenLabs Conversational AI and Twilio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luke-deltadesk](https://clawhub.ai/user/luke-deltadesk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up and run ElevenLabs Conversational AI phone-call workflows through shell commands. It lists agents and phone numbers, places outbound calls, and retrieves conversation transcripts or audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real outbound AI phone calls through an ElevenLabs account. <br>
Mitigation: Use a dedicated or revocable API key, verify the recipient number and call purpose before execution, and confirm consent and legal requirements for the call. <br>
Risk: Conversation transcripts and audio recordings may contain sensitive data and can appear in terminal output, logs, or saved files. <br>
Mitigation: Treat transcripts and audio as sensitive data, restrict where outputs are stored or logged, and follow applicable call-recording and privacy requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/luke-deltadesk/elevenlabs-calls) <br>
- [ElevenLabs Agents Platform Overview](https://elevenlabs.io/docs/agents-platform/overview) <br>
- [ElevenLabs Agents](https://elevenlabs.io/app/agents) <br>
- [ElevenLabs Phone Numbers](https://elevenlabs.io/app/agents/phone-numbers) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance, JSON, Audio files] <br>
**Output Format:** [Markdown instructions with bash command examples; scripts return terminal text, JSON, or audio bytes depending on the command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ELEVENLABS_API_KEY plus curl and jq. Some commands can initiate paid outbound calls or expose transcripts and recordings.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
