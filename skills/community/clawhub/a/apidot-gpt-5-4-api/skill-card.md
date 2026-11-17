## Description:

Use APIDot for GPT 5.4 API workflows, including OpenAI-compatible chat, professional task execution, spreadsheet and document analysis, tool-oriented planning, code and test handoffs, streaming planning, usage tracking, API key safety guidance, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route GPT 5.4 integration questions to APIDot documentation, model pages, examples, and implementation planning guidance. It supports planning for chat behavior, spreadsheet and document analysis, streaming, usage tracking, and API key handling without making API calls itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the package as an executable APIDot integration rather than documentation guidance.

Mitigation: Use it only as a documentation router and verify current APIDot docs before implementation or production decisions.

Risk: APIDOT_API_KEY or private prompts, documents, tool inputs, generated responses, usage records, or request IDs could be exposed in client code, logs, screenshots, repositories, or chat output.

Mitigation: Keep API keys server-side only, use a backend secret manager or environment variable, and keep sensitive request and response data out of public logs and outputs.

Risk: Model-specific request fields, availability, limits, or commercial terms may be stale if copied from the local reference.

Mitigation: Check the live APIDot model page and API documentation before preparing payloads or making production decisions.

## Reference(s):

- [APIDot GPT 5.4 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot GPT 5.4 Model Page](https://apidot.ai/models/gpt-5-4)
- [APIDot GPT 5.4 API Docs](https://apidot.ai/docs/gpt-5-4)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Error Guidance](https://apidot.ai/docs/errors)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with documentation links and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable files, bundled API client, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
