## Description:

Use APIDot for chat API workflows, including OpenAI-compatible chat completions, coding assistants, reasoning models, multimodal assistant routing, streaming planning, server-side API key safety, and APIDot chat model docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route APIDot chat integration questions to the relevant docs, model pages, examples, and server-side API-key safety guidance. It supports planning for chat completions, coding assistants, reasoning workflows, multimodal chat, streaming, request storage, and rate-limit handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Store APIDOT_API_KEY only in server-side environment variables or an approved secret manager, and avoid echoing credentials in generated examples or logs.

Risk: Live APIDot API calls could be made unintentionally while following integration guidance.

Mitigation: Make live API calls only when explicitly requested and when a safe server-side environment is available.

Risk: APIDot model availability, request fields, or product details may change after the skill release.

Mitigation: Check the current APIDot docs and model catalog before selecting model-specific routes or making product claims.

## Reference(s):

- [APIDot API Docs](https://apidot.ai/docs)
- [APIDot Chat Models](https://apidot.ai/models/chat)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [APIDot GitHub Organization](https://github.com/APIDotAI)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional code, shell command, or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable files, automatic network calls, install-time automation, or credential storage.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
