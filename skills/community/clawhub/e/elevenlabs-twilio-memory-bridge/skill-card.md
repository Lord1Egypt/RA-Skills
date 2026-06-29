## Description: <br>
FastAPI personalization webhook that adds persistent caller memory and dynamic context injection to ElevenLabs Conversational AI agents on Twilio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[britrik](https://clawhub.ai/user/britrik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to deploy a small FastAPI webhook that injects caller memory, session history, and daily notes into ElevenLabs Conversational AI calls routed through Twilio. It supports OpenClaw or another OpenAI-compatible LLM endpoint while leaving real-time audio handling to ElevenLabs and Twilio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service handles caller-linked memories, notes, and configured API keys as sensitive data. <br>
Mitigation: Use strong webhook and admin secrets, scope API keys to minimum required permissions, and define caller notice, retention, and deletion procedures before production use. <br>
Risk: Memories and notes are stored as plain JSON unless DATA_ENCRYPTION_KEY is configured. <br>
Mitigation: Set DATA_ENCRYPTION_KEY in production and protect the data directory with the documented restrictive file permissions. <br>
Risk: The bridge is a public web service with webhook and admin endpoints. <br>
Mitigation: Require webhook HMAC verification, protect admin endpoints with ADMIN_API_KEY, keep CORS restricted, and serve both the bridge and LLM endpoint over HTTPS. <br>
Risk: Injected soul templates and memory context can influence caller-facing behavior and may contain sensitive details. <br>
Mitigation: Review and customize the soul template before deployment and use trusted LLM endpoints for personalized calls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/britrik/skills/elevenlabs-twilio-memory-bridge) <br>
- [Project Homepage](https://github.com/britrik/elevenlabs-twilio-memory-bridge) <br>
- [ElevenLabs Agents Dashboard](https://elevenlabs.io/app/agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration details, and Python/FastAPI service code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment and configuration guidance for a webhook service that stores caller-linked memory in local JSON files when run.] <br>

## Skill Version(s): <br>
1.2.1 (source: ClawHub release metadata; artifact frontmatter and manifest list 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
