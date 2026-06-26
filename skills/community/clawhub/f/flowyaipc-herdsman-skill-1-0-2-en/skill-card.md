## Description: <br>
Integration package for the Herdsman model engine that helps agent platforms call local OpenAI, Anthropic Messages, and AG-UI compatible services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiejingke](https://clawhub.ai/user/jiejingke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent platform maintainers use this skill to integrate Herdsman as a local model backend for chat, image generation and editing, OCR, embeddings, reranking, speech transcription, text-to-speech, and voice cloning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice cloning can be misused for impersonation or unauthorized synthesis. <br>
Mitigation: Use only authorized reference audio and require review of voice cloning requests before running TTS voice clone scripts. <br>
Risk: Media conversion, OCR, transcription, and generation scripts can read local files and write outputs. <br>
Mitigation: Restrict script access to expected input and output directories, and check output paths before running conversion or save commands. <br>
Risk: Calling untrusted Herdsman base URLs can expose prompts, media, credentials, or generated outputs. <br>
Mitigation: Prefer local 127.0.0.1 endpoints and avoid untrusted base URLs unless the deployment owner has reviewed the service. <br>
Risk: The security scan verdict is suspicious because sensitive media workflows need user review before installation. <br>
Mitigation: Install only when the publisher is trusted and the deployment needs Herdsman media integration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiejingke/flowyaipc-herdsman-skill-1-0-2-en) <br>
- [Herdsman API Call Examples](artifact/references/api-examples.md) <br>
- [Herdsman Platform Integration Guide](artifact/references/platform-integration.md) <br>
- [Herdsman Model Capabilities](artifact/references/model-capabilities.md) <br>
- [Herdsman Error Code Reference](artifact/references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python scripts, command examples, JSON responses, and generated media or transcription files when scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may call local Herdsman endpoints, read local media inputs, and write generated image, audio, OCR, or transcription outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
