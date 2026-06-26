## Description: <br>
FastAPI personalization webhook that adds persistent caller memory and dynamic context injection to ElevenLabs Conversational AI agents on Twilio. No audio proxying, file-based persistence, OpenClaw compatible. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[britrik](https://clawhub.ai/user/britrik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and voice-agent operators use this skill to deploy a FastAPI bridge that injects caller memory, session history, and daily notes into ElevenLabs Conversational AI agents connected through Twilio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The public personalization webhook can run without authentication while returning stored caller context. <br>
Mitigation: Use WEBHOOK_SECRET for every non-local deployment, serve the bridge only over HTTPS, and restrict network exposure where possible. <br>
Risk: The service stores caller memories and notes that may contain sensitive personal context. <br>
Mitigation: Establish caller consent, retention, deletion, and access-control processes before production use. <br>
Risk: The deployment depends on sensitive API keys and admin credentials. <br>
Mitigation: Use scoped credentials, load secrets only from environment variables, and set a strong ADMIN_API_KEY for administrative endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/britrik/elevenlabs-twilio-memory-bridge) <br>
- [Project homepage](https://github.com/britrik/elevenlabs-twilio-memory-bridge) <br>
- [ElevenLabs Agents dashboard](https://elevenlabs.io/app/agents) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Code, API responses] <br>
**Output Format:** [Markdown guidance with shell commands, Python service files, environment configuration, and JSON webhook/API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10+, FastAPI, uvicorn, ElevenLabs and Twilio accounts, OpenClaw or another OpenAI-compatible LLM endpoint, HTTPS public access, and sensitive environment credentials.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
