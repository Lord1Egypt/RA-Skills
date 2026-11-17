## Description:

Use APIDot for Flux Schnell API workflows, including FLUX.1 Schnell, Black Forest Labs image generation, fast low-cost text-to-image drafts, prompt exploration, batch creative iteration, task_id, polling, webhooks, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Flux Schnell integration questions to APIDot documentation, model pages, async workflow guidance, polling, webhook delivery, and API-key handling guidance for fast text-to-image draft workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or sensitive workflow data could be exposed if users place APIDOT_API_KEY, prompts, callback URLs, task IDs, or generated image URLs in client code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager, and avoid logging or publicly sharing prompts, callback URLs, task IDs, generated image URLs, or customer data.

Risk: Flux Schnell payload fields, availability, limits, or commercial terms may change outside the artifact.

Mitigation: Use the current APIDot docs and model page as the source of truth before preparing request payloads or making product claims.

Risk: Live API calls could be made from an unsafe environment if the skill's guidance is applied without checking execution context.

Mitigation: Treat the skill as documentation support, not an API client, and make live API calls only when the user explicitly asks and has a safe server-side environment.

## Reference(s):

- [APIDot Flux Schnell Reference](references/api.md)
- [APIDot Flux Schnell model page](https://apidot.ai/models/flux-schnell)
- [APIDot Flux Schnell API docs](https://apidot.ai/docs/flux-schnell)
- [APIDot docs](https://apidot.ai/docs)
- [APIDot quickstart](https://apidot.ai/docs/quickstart)
- [APIDot webhooks](https://apidot.ai/docs/webhooks)
- [APIDot examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with links, integration notes, and copyable code or shell command suggestions when requested by the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; it includes no executable automation, bundled clients, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
