## Description:

Redact PII from text locally using a fine-tuned 1B SLM while keeping sensitive text on the user's machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jgolebiowski](https://clawhub.ai/user/jgolebiowski)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to redact personal data from text before sharing or processing it with an agent. It is suited for local anonymization workflows that need redacted text output and, when explicitly requested, detected-entity mappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Redaction may miss payment data or regulated PII, including cases where examples leave a full card number visible.

Mitigation: Review redacted output before sharing, avoid treating the result as guaranteed sanitized, and add separate checks for payment data or regulated identifiers.

Risk: The --show-entities mode returns original PII values in JSON.

Mitigation: Use --show-entities only when entity mappings are explicitly required, and avoid displaying or storing that JSON in normal redaction workflows.

Risk: Setup downloads and runs a local model from Hugging Face.

Mitigation: Pin and verify the model artifact before setup when supply-chain assurance is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jgolebiowski/skills/distil-open-claw-pii)
- [Distil-PII GitHub repository](https://github.com/distil-labs/Distil-PII)
- [Distil-PII Hugging Face collection](https://huggingface.co/distil-labs)
- [Distil-PII Llama 3.2 3B GGUF model](https://huggingface.co/distil-labs/Distil-PII-Llama-3.2-3B-Instruct-gguf)
- [Distil-PII Gemma 270M GGUF model](https://huggingface.co/distil-labs/Distil-PII-gemma-3-270m-it-gguf)
- [llama.cpp build instructions](https://github.com/ggerganov/llama.cpp#build)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text by default; JSON when entity mappings are explicitly requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output suppresses original entity values; --show-entities returns original values in JSON.]

## Skill Version(s):

1.1.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
