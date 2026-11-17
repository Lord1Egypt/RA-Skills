## Description:

Build and manage ElevenLabs Conversational AI voice agents with Twilio phone integration for phone agents, voice and LLM configuration, sales flows, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boris148](https://clawhub.ai/user/boris148)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and sales teams use this skill to create, configure, test, and troubleshoot ElevenLabs phone agents connected to Twilio numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to use broad Twilio credentials and connect or change phone-number routing.

Mitigation: Use test numbers and least-privilege credentials where possible, keep Twilio Auth Tokens out of chats and logs, and require explicit approval before creating, purchasing, connecting, or changing any production phone number or agent routing.

Risk: The release is flagged suspicious by the server security summary because it does not include enough safety guidance for real ElevenLabs or Twilio accounts.

Mitigation: Review the skill before installing or using it with real accounts, and apply account, credential, and routing controls before deployment.

## Reference(s):

- [ElevenLabs Conversational AI agent create endpoint](https://api.elevenlabs.io/v1/convai/agents/create)
- [ElevenLabs Conversational AI agent endpoint](https://api.elevenlabs.io/v1/convai/agents/{agent_id})
- [ElevenLabs Twilio phone numbers endpoint](https://api.elevenlabs.io/v1/convai/twilio/phone-numbers)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls]

**Output Format:** [Markdown guidance with API endpoint examples and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include phone-agent setup steps, voice and LLM settings, sales prompt guidance, Twilio connection steps, and troubleshooting advice.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
