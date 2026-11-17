## Description:

Use when designing, configuring, or implementing applications targeting the Google Gemma 4 model family. Covers model architecture selection (26B/12B/E2B/E4B), native Thinking Mode formatting, function calling schemas, multimodal audio/vision pipelines, and deployment reference patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johngreenfield](https://clawhub.ai/user/johngreenfield)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to select Gemma 4 model variants, structure thinking-mode and tool-calling prompts, integrate multimodal inputs, and adapt local, browser, or Vertex AI deployment examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reasoning traces can expose internal prompts or sensitive data if shown to end users.

Mitigation: Keep thought output restricted to developer-only tools and use the provided fail-closed stream parser before rendering user-facing responses.

Risk: Cloud deployment examples may transmit prompts to Vertex AI and model examples may contact declared external model hosts.

Mitigation: Use approved projects and regions, avoid sensitive data unless policy allows it, and review the declared egress endpoints before deployment.

Risk: Adapting examples without pinned artifacts can weaken supply-chain controls.

Mitigation: Keep immutable model and tokenizer revisions, keep trust_remote_code disabled where shown, and pin package versions when integrating the examples.

## Reference(s):

- [Gemma 4 Hardware Sizing and VRAM Matrix](references/hardware-sizing.md)
- [Gemma 4 Native Multimodal Integration](references/multimodal.md)
- [ClawHub skill release page](https://clawhub.ai/johngreenfield/skills/gemma4-dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, configuration notes, and reference snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model sizing guidance, prompt formats, stream parser usage, and deployment snippets.]

## Skill Version(s):

1.0.4 (source: server release evidence and openclaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
