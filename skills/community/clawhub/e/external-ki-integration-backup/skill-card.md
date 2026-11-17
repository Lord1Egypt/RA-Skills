## Description:

Skill for accessing external AI services (ChatGPT, Claude, Hugging Face, etc.) via browser automation (Chrome Relay) and APIs to assist with tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[konscious0beast](https://clawhub.ai/user/konscious0beast)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to consult external AI services through authorized browser sessions or API keys for reasoning, code generation, summarization, and analysis tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected prompts or content may be sent to external AI services through logged-in browser sessions or API keys.

Mitigation: Use the skill only after explicitly approving the exact data to share, and avoid confidential, personal, financial, credential, or proprietary data unless sharing is intentionally authorized.

Risk: Prompt and response persistence may retain sensitive interaction details without enough scoping controls.

Mitigation: Disable or restrict memory logging of prompts and responses when using external services.

Risk: External APIs or subscribed web sessions can incur costs or hit provider rate limits.

Mitigation: Use paid APIs only with explicit authorization, monitor estimated usage, and respect service rate limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/konscious0beast/skills/external-ki-integration-backup)
- [OpenClaw Browser Relay docs](https://docs.openclaw.ai/browser-relay)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text responses with optional code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on user-provided browser sessions or API keys; external service terms, rate limits, and costs apply.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
