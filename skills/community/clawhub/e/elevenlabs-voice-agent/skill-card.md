## Description: <br>
Build and manage ElevenLabs Conversational AI voice agents with Twilio phone integration for AI phone agents, voice and LLM settings, phone-number connection, and voice-agent troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boris148](https://clawhub.ai/user/boris148) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure ElevenLabs conversational phone agents, connect Twilio phone numbers, tune voice and LLM settings, and troubleshoot common call-quality issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Twilio Auth Tokens or other phone integration credentials could be exposed through chat messages, committed files, logs, or screenshots. <br>
Mitigation: Keep credentials in a secret manager or environment variables, avoid pasting them into agent chats, and redact them from logs and screenshots. <br>
Risk: Agent creation, updates, or Twilio number connections can affect live call routing. <br>
Mitigation: Confirm each create, update, and phone-number connection before execution, test routing with controlled numbers, monitor active call behavior, and disconnect unused agents or numbers. <br>


## Reference(s): <br>
- [ElevenLabs create conversational agent endpoint](https://api.elevenlabs.io/v1/convai/agents/create) <br>
- [ElevenLabs conversational agent endpoint](https://api.elevenlabs.io/v1/convai/agents/{agent_id}) <br>
- [ElevenLabs Twilio phone number endpoint](https://api.elevenlabs.io/v1/convai/twilio/phone-numbers) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes recommended voice settings, Twilio connection steps, phone-agent feature guidance, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
