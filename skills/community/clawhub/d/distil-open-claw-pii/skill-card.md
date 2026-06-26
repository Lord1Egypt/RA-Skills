## Description: <br>
Redact PII from text locally using a fine-tuned 1B SLM. Text never leaves your machine. Handles names, emails, phones, addresses, SSNs, credit cards, IBANs, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jgolebiowski](https://clawhub.ai/user/jgolebiowski) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to redact, anonymize, sanitize, or remove personal data from text while keeping raw input on the local machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads a large model and runs a local llama.cpp background server on port 8712. <br>
Mitigation: Install only in an approved local environment, confirm the model download and server process are acceptable, and stop the server with scripts/stop.sh when finished. <br>
Risk: Automated PII redaction can miss sensitive values or preserve details that still identify a person. <br>
Mitigation: Review redacted output before sharing or storing it, especially for regulated or high-sensitivity data. <br>
Risk: The --show-entities mode returns original PII values in JSON output. <br>
Mitigation: Use --show-entities only when original-value mappings are explicitly needed, and treat that output as sensitive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jgolebiowski/distil-open-claw-pii) <br>
- [llama.cpp build documentation](https://github.com/ggerganov/llama.cpp#build) <br>
- [Default Distil-PII 1B GGUF model](https://huggingface.co/distil-labs/Distil-PII-Llama-3.2-1B-Instruct-gguf/resolve/main/model.gguf) <br>
- [Distil-PII Llama 3.2 3B GGUF model](https://huggingface.co/distil-labs/Distil-PII-Llama-3.2-3B-Instruct-gguf) <br>
- [Distil-PII Gemma 270M GGUF model](https://huggingface.co/distil-labs/Distil-PII-gemma-3-270m-it-gguf) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text by default; JSON when --show-entities is explicitly requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output omits original PII values; --show-entities includes original-value entity mappings.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
