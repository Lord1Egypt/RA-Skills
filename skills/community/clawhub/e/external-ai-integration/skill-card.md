## Description:

Leverage external AI models such as ChatGPT, Claude, Gemini, and Hugging Face-hosted models as on-demand tools through browser automation and optional Hugging Face API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[konscious0beast](https://clawhub.ai/user/konscious0beast)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to route suitable tasks to external AI services for second opinions, summarization, translation, code review, brainstorming, and other specialized model-assisted work while keeping the main agent in control of the workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts or workspace content may be sent to third-party AI services without an explicit sensitivity gate.

Mitigation: Use only non-sensitive prompts by default, or require approval and redaction before any external AI call.

Risk: Credentials used for Hugging Face or browser-based services could be exposed through broad configuration paths, curl usage, or logs.

Mitigation: Use narrowly scoped tokens from a controlled configuration path, avoid the curl fallback, and do not log token fragments.

Risk: External AI responses may be incorrect, misleading, or unsuitable for direct use in higher-impact decisions.

Mitigation: Validate external model outputs before incorporating them into final answers, code changes, or operational guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/konscious0beast/skills/external-ai-integration)
- [Skill instructions](artifact/SKILL.md)
- [External AI integration implementation](artifact/external_ai_integration.py)
- [ChatGPT web application](https://chatgpt.com)
- [Hugging Face Inference API endpoint pattern](https://api-inference.huggingface.co/models/{model})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; external service responses may be returned as text or JSON-like API payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May incorporate outputs from third-party AI services; no fixed token or response-size limits are specified.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
