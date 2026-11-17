## Description:

Routes agents to APIDot Claude 4.6 documentation and guidance for Messages API, chat completions, streaming, tool use planning, production chat, coding agents, and API key safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill to plan APIDot Claude 4.6 integrations, find model docs and examples, and apply API key handling guidance before making backend API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys or private request data could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in a backend secret store or server-side environment variable, and avoid logging API keys, private prompts, customer data, tool arguments, private context, or generated responses.

Risk: Agents could produce stale or incorrect Claude 4.6 request details, model availability claims, limits, or commercial terms.

Mitigation: Use current APIDot docs and model pages as the source of truth before preparing copyable request examples or product-specific guidance.

Risk: A live APIDot API call could be made before the user intends to connect their application.

Mitigation: Only make live API calls when the user explicitly asks and provides a safe server-side environment.

## Reference(s):

- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Claude 4.6 Model Page](https://apidot.ai/models/claude-4-6)
- [APIDot Claude 4.6 Docs](https://apidot.ai/docs/claude-4-6)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Error Guidance](https://apidot.ai/docs/errors)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [APIDot Claude 4.6 Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with documentation links and safety notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable files, bundled API clients, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
