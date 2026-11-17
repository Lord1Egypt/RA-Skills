## Description:

FastAPI personalization webhook that adds persistent caller memory and dynamic context injection to ElevenLabs Conversational AI agents on Twilio without proxying audio, using file-based persistence and OpenClaw-compatible LLM routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[britrik](https://clawhub.ai/user/britrik)

### License/Terms of Use:

MIT

## Use Case:

Developers and voice-agent operators use this skill to deploy a personalization bridge for inbound Twilio calls handled by ElevenLabs agents. It lets an agent retrieve caller history, long-term facts, and daily notes before a conversation starts while using OpenClaw or another OpenAI-compatible LLM backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge persists sensitive caller context and long-term memory.

Mitigation: Review the data handling model before deployment, enable DATA_ENCRYPTION_KEY in production, define retention and deletion procedures, and provide appropriate caller notice or consent.

Risk: Stored memories and notes are injected into agent system prompts.

Mitigation: Restrict who can write memories or global notes, review stored entries for prompt-injection text, and treat memory updates as trusted administrative actions.

Risk: Webhook and admin endpoints depend on deployment secrets.

Mitigation: Keep ADMIN_API_KEY, WEBHOOK_SECRET, and PHONE_HASH_SALT strong and private, use HTTPS, and use scoped API keys for ElevenLabs and OpenClaw.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/britrik/skills/elevenlabs-twilio-memory-bridge)
- [Project homepage](https://github.com/britrik/elevenlabs-twilio-memory-bridge)
- [ElevenLabs Agents dashboard](https://elevenlabs.io/app/agents)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python/FastAPI code, shell commands, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires environment variables for ElevenLabs, OpenClaw, public service URL, admin authentication, webhook verification, and phone hashing.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter and manifest report 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
