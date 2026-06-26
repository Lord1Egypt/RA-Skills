## Description: <br>
DigenAI image and video generation for OpenClaw, supporting text-to-image, image-to-video, and text-to-video API workflows with DigenAI credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eeoeofl](https://clawhub.ai/user/eeoeofl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call DigenAI APIs for image generation, video generation, image upload, batch generation, and generation-status polling from an OpenClaw agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled Discord and Telegram bot assets include runnable key-issuing flows and hardcoded live-looking secrets. <br>
Mitigation: Do not run the bot scripts as packaged; rotate any exposed credentials, remove packaged secrets, and require operators to inject fresh credentials through a secure secret manager. <br>
Risk: Credential handling stores user API keys in local plaintext files for the bot workflows. <br>
Mitigation: Replace plaintext key storage with access-controlled encrypted storage and minimize retained user key data before deployment. <br>
Risk: Some API paths disable TLS certificate verification for the older DigenAI API client. <br>
Mitigation: Restore TLS verification and fail closed on certificate errors before using the old image-generation API in production. <br>
Risk: Prompts, uploaded files, generated media URLs, and long URLs may be sent to DigenAI services and TinyURL. <br>
Mitigation: Disclose outbound data flows to users, avoid sensitive inputs, and review third-party API terms before commercial use. <br>


## Reference(s): <br>
- [DigenAI API Reference](references/api.md) <br>
- [DigenAI API Key Portal](https://claw.digen.ai) <br>
- [Digen Ai Free on ClawHub](https://clawhub.ai/eeoeofl/digen-ai-free) <br>
- [DigenAI Discord Key Channel](https://discord.gg/SRhbTt9hwp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell environment setup, and JSON-like API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media URLs, task identifiers, status values, thumbnails, and error messages may be returned by the DigenAI APIs.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
