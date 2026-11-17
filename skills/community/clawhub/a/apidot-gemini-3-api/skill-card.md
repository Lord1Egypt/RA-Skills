## Description:

Use APIDot for Gemini 3 API workflows, including Gemini 3 Flash Preview, Gemini 3 Pro Preview, native generateContent, streamGenerateContent, Gemini chat, coding assistants, streaming, tool planning, API key safety guidance, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Gemini 3 integration work through APIDot documentation, model pages, examples, and API key safety guidance. It helps plan Gemini 3 chat, generateContent, streaming, coding assistant, support assistant, and tool-planning workflows without making live API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY or private Gemini workflow data could be exposed in client code, logs, screenshots, repositories, or chat output.

Mitigation: Keep API keys in server-side environment variables or a backend secret manager, and avoid logging prompts, outputs, credentials, private context, customer data, tool arguments, or media references.

Risk: Gemini 3 request fields, model availability, limits, or commercial terms may change outside the static skill artifact.

Mitigation: Verify the current APIDot Gemini 3 docs and model pages before preparing live requests or making product claims.

Risk: Incorrect retry behavior could amplify invalid requests or make task-style workflows inconsistent.

Mitigation: Retry only transient network failures with backoff, do not retry invalid payloads unchanged, and preserve task identifiers for idempotent status or callback handling when a task-style flow is used.

## Reference(s):

- [APIDot Gemini 3 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Gemini 3 Model Page](https://apidot.ai/models/gemini-3)
- [APIDot Gemini 3 API Docs](https://apidot.ai/docs/gemini-3)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Error Guidance](https://apidot.ai/docs/errors)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with links, API planning notes, and optional code or configuration suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; includes no executable files, bundled API clients, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
