## Description:

Claude 4.5 API on APIDot for Claude Opus 4.5, Claude Sonnet 4.5, Claude Haiku 4.5, Claude 4 5, claude-4-5, Messages API, chat completions, streaming, tool use, coding agents, production chat, API key safety, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this documentation-only skill to route Claude 4.5 integration questions to APIDot model pages, docs, examples, and implementation guidance. It supports planning production chat, coding-agent, tool-use, streaming, and long-context workflows without making live API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys may be exposed if copied into browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager and avoid logging prompts, tool inputs, generated outputs, or credentials.

Risk: Claude 4.5 request fields, model availability, limits, or commercial terms may change over time.

Mitigation: Verify the current APIDot model page and docs before making live requests or publishing integration examples.

## Reference(s):

- [APIDot Claude 4.5 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Claude 4.5 Model Page](https://apidot.ai/models/claude-4-5)
- [APIDot Claude 4.5 Docs](https://apidot.ai/docs/claude-4-5)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Error Guidance](https://apidot.ai/docs/errors)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with links, code snippets, shell commands, and configuration notes when requested by the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; it does not execute code, make network requests, or store credentials.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
