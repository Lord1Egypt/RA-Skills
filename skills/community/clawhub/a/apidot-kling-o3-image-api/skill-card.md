## Description:

Use APIDot for Kling O3 Image API workflows, including text-to-image API, image editing API, reference-guided image generation, element control, 1K, 2K, or 4K output planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan APIDot Kling O3 Image integrations, route to the right APIDot documentation, and handle async image generation, editing, polling, and webhook workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or private generation inputs could be exposed if copied into browser code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY and private prompts or image URLs server-side in environment variables or a secret manager, and avoid logging sensitive request data.

Risk: Model fields, limits, pricing, or availability may change outside this documentation-only release.

Mitigation: Review the current APIDot docs and model page before making live API calls or committing request shapes.

Risk: Async image workflows can lose state or duplicate visible results if task IDs and webhook events are not handled carefully.

Mitigation: Persist task_id, request status, selected model, media references, and final image URLs together, and make webhook handlers idempotent.

## Reference(s):

- [APIDot docs](https://apidot.ai/docs)
- [Kling O3 Image model page](https://apidot.ai/models/kling-o3-image)
- [Kling O3 Image API docs](https://apidot.ai/docs/kling-o3-image)
- [APIDot quickstart](https://apidot.ai/docs/quickstart)
- [APIDot webhooks](https://apidot.ai/docs/webhooks)
- [APIDot examples](https://github.com/APIDotAI/apidot-examples)
- [APIDot Kling O3 Image Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with links, request-planning notes, and implementation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable code, install automation, credential storage, or automatic network calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
