## Description:

Integration package for the Herdsman model engine. Used by other agent platforms to call scripts in this directory and protocol specifications when connecting to OpenAI, Anthropic, or AGUI-compatible services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiejingke](https://clawhub.ai/user/jiejingke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-platform integrators use this skill to connect agents to a Herdsman local model engine through OpenAI-compatible, Anthropic Messages-compatible, and AG-UI endpoints. It supports text, image, OCR, embedding, rerank, transcription, speech synthesis, and voice-cloning workflows through reusable Python scripts and protocol notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be sent when media is downloaded from untrusted URLs.

Mitigation: Use only trusted Herdsman or cache endpoints for downloads, avoid auto-downloading media from untrusted services, and prefer empty or scoped API keys.

Risk: Generated or downloaded files may be written with little containment.

Mitigation: Keep outputs in a dedicated directory and review any explicit output paths before allowing an agent to write files.

Risk: Images, audio, voices, and business documents submitted through the skill are processed by the configured service.

Mitigation: Do not submit sensitive media, voices, or documents unless that processing is intended and approved.

## Reference(s):

- [Herdsman API Call Examples](artifact/references/api-examples.md)
- [Herdsman Platform Integration Guide](artifact/references/platform-integration.md)
- [Herdsman Model Capabilities](artifact/references/model-capabilities.md)
- [Herdsman Error Code Reference](artifact/references/error-codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; scripts may emit text, JSON, URLs, or saved media file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call configured Herdsman endpoints and write generated image, audio, OCR, or transcription outputs to local paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
