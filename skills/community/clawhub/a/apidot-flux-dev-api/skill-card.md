## Description:

Use APIDot for Flux Dev API workflows, including FLUX.1 Dev, Black Forest Labs image generation, text-to-image, single-reference image-to-image, prompt adherence, realistic detail, task_id, polling, webhooks, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route FLUX.1 Dev image-generation work through APIDot documentation, including text-to-image, single-reference image-to-image, async task polling, and webhook planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if copied into frontend code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager and avoid echoing it in generated examples.

Risk: Prompts, source image URLs, generated image URLs, callback URLs, and task IDs may contain sensitive user or workflow data.

Mitigation: Treat those values as sensitive, minimize logging, and store request status and final image references in backend-controlled systems.

Risk: Model request fields, availability, limits, or commercial terms may change outside the packaged documentation summary.

Mitigation: Check current APIDot model pages and API docs before preparing payloads or making real API calls.

## Reference(s):

- [APIDot documentation](https://apidot.ai/docs)
- [Flux Dev model page](https://apidot.ai/models/flux-dev)
- [Flux Dev API docs](https://apidot.ai/docs/flux-dev)
- [APIDot quickstart](https://apidot.ai/docs/quickstart)
- [APIDot webhooks](https://apidot.ai/docs/webhooks)
- [APIDot examples](https://github.com/APIDotAI/apidot-examples)
- [APIDot Flux Dev Reference](references/api.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no bundled executable files, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
