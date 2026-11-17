## Description:

Use APIDot for Claude Opus 4.8 API workflows, including Claude Messages, long-context reasoning, complex coding, long-horizon agents, adaptive thinking, streaming planning, tool-use planning, API key safety guidance, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan APIDot Claude Opus 4.8 integrations, route to current APIDot documentation, and handle request planning, streaming, tool use, and API key safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Store APIDOT_API_KEY only in server-side environment variables or a backend secret manager, and avoid echoing credentials in generated guidance.

Risk: Prompts, source documents, customer data, tool inputs, generated responses, usage records, and request IDs may be sensitive when sent to external APIs.

Mitigation: Treat API inputs and outputs as sensitive by default, keep live calls in an appropriate server-side environment, and avoid public logging of private request or response data.

## Reference(s):

- [APIDot Claude Opus 4.8 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [Claude Opus 4.8 Model Page](https://apidot.ai/models/claude-opus-4-8)
- [Claude Opus 4.8 API Docs](https://apidot.ai/docs/claude-opus-4-8)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Error Guidance](https://apidot.ai/docs/errors)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with links and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable output or live API calls.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
