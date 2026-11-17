## Description:

Generate product descriptions using free AI backends, either Ollama locally or the HuggingFace Inference API online.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create e-commerce product copy from a product name and feature list. It supports a private local Ollama backend by default and an optional HuggingFace backend for online generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential or unreleased product names and features could be sent to HuggingFace when the online backend is selected.

Mitigation: Use the default Ollama backend for private product information; choose HuggingFace only when the inputs are appropriate to share with that service.

Risk: Installing runtime dependencies from untrusted sources can expose the execution environment.

Mitigation: Install dependencies in an isolated environment from trusted package sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/ai-product-description-generator-free)
- [BytesAgain homepage](https://bytesagain.com)
- [Ollama](https://ollama.ai)
- [HuggingFace Inference API model endpoint](https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text with a title, short description, and bullet-point features]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports professional, casual, and SEO styles; uses local Ollama by default or HuggingFace when selected.]

## Skill Version(s):

2.0.1 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
