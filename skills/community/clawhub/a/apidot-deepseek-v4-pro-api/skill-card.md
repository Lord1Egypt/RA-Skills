## Description:

Use APIDot for DeepSeek V4 Pro API workflows, including OpenAI-compatible chat, 1M-token long-context reasoning, complex coding, document review, agent planning, streaming planning, usage tracking, API key safety guidance, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route DeepSeek V4 Pro integration work through APIDot documentation, including OpenAI-compatible chat planning, long-context reasoning, coding workflows, document review, streaming behavior, usage tracking, and API key handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY, prompts, customer data, documents, generated responses, usage records, or request IDs could be exposed if copied into client code, public logs, screenshots, repositories, or chat output.

Mitigation: Keep API keys in server-side environment variables or a backend secret manager, treat user and request data as sensitive, and avoid logging secrets or private content.

Risk: The skill routes API integration work but does not make live calls or verify current APIDot product details itself.

Mitigation: Use the current APIDot docs and model page before making live calls, choosing request fields, or relying on model availability, limits, pricing, or commercial terms.

## Reference(s):

- [APIDot DeepSeek V4 Pro Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [DeepSeek V4 Pro Docs](https://apidot.ai/docs/deepseek-v4-pro)
- [DeepSeek V4 Pro Model Page](https://apidot.ai/models/deepseek-v4-pro)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Error Guidance](https://apidot.ai/docs/errors)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with documentation links and integration checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no bundled executable code or live API calls.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
