## Description:

Use APIDot for GPT 5.2 API workflows, including OpenAI-compatible chat, legacy professional-work compatibility, 400K-token long-context synthesis, agentic coding handoffs, chart reasoning, streaming planning, usage tracking, API key safety guidance, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route GPT 5.2 integration questions to APIDot documentation, model pages, examples, and safe implementation guidance for chat, long-context synthesis, streaming planning, usage tracking, and coding handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys or private prompts, documents, customer data, tool inputs, generated responses, usage records, or request IDs could be exposed through unsafe handling.

Mitigation: Keep APIDOT_API_KEY server-side only, use a backend secret manager or environment variable, and avoid placing sensitive inputs or outputs in browser code, public repositories, logs, screenshots, or chat output.

Risk: Model availability, request fields, limits, reliability, performance, or commercial terms may change after the skill release.

Mitigation: Verify current product details in the live APIDot docs and model page before preparing payloads or making claims.

## Reference(s):

- [APIDot GPT 5.2 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot GPT 5.2 Model Page](https://apidot.ai/models/gpt-5-2)
- [APIDot GPT 5.2 API Docs](https://apidot.ai/docs/gpt-5-2)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Error Guidance](https://apidot.ai/docs/errors)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions]

**Output Format:** [Markdown guidance with links and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no executable files, stored credentials, or automatic network calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
