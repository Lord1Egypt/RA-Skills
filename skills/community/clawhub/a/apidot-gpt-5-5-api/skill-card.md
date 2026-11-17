## Description:

Use APIDot for GPT 5.5 API workflows, including OpenAI-compatible chat, long-horizon agentic execution, complex coding, research synthesis, document analysis, streaming planning, usage tracking, API key safety guidance, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route GPT 5.5 integration questions to APIDot documentation and plan backend API workflows, including chat handling, streaming behavior, usage tracking, and API-key safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY, private prompts, source documents, customer data, tool inputs, generated responses, usage records, or request IDs could be exposed if copied into frontend code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in a server-side secret store and treat prompts, documents, tool inputs, generated responses, usage records, and request IDs as sensitive unless the user explicitly says they can be shared.

Risk: Live API calls or guessed GPT 5.5 request fields could create cost, reliability, or correctness issues.

Mitigation: Make live APIDot calls only when the user explicitly requests them in a safe server-side environment, and use the current APIDot model page and docs for supported fields, availability, limits, and commercial terms.

## Reference(s):

- [APIDot GPT 5.5 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot GPT 5.5 Model Page](https://apidot.ai/models/gpt-5-5)
- [APIDot GPT 5.5 Docs](https://apidot.ai/docs/gpt-5-5)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Error Guidance](https://apidot.ai/docs/errors)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with links and optional backend code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no bundled clients, scripts, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
