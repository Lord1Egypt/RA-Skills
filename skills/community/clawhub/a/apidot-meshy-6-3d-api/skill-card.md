## Description:

Use APIDot for Meshy 6 3D API workflows, including Meshy 6 API, text-to-3D API, image-to-3D API, multi-image-to-3D API, 3D asset generation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Meshy 6 3D API integration questions to APIDot documentation, examples, and async workflow guidance for text-to-3D, image-to-3D, multi-image-to-3D, polling, and webhook handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or private prompts, media URLs, callback URLs, or generated asset URLs could be exposed if copied into frontend code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in a backend environment or secret manager, avoid logging sensitive request data or generated asset URLs, and treat callback URLs as sensitive integration details.

Risk: APIDot Meshy 6 request fields, model availability, limits, or commercial terms may change after this documentation-only skill is installed.

Mitigation: Verify the current APIDot docs and model page before implementing payload fields, retry behavior, webhook handling, or production commercial assumptions.

Risk: Async 3D jobs can produce duplicate or inconsistent records if task IDs, status transitions, retries, or webhook callbacks are handled loosely.

Mitigation: Persist task_id with the selected model, user, source media, status, and final asset URLs; make webhook handlers idempotent and retry only transient failures with backoff.

## Reference(s):

- [APIDot Meshy 6 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Meshy 6 3D Docs](https://apidot.ai/docs/meshy-6-3d)
- [APIDot Meshy 6 Model Page](https://apidot.ai/models/meshy-6-3d)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-meshy-6-3d-api)
- [Publisher Profile](https://clawhub.ai/user/jiehao71727)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with API integration notes and optional code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; does not execute code, make network requests, or store credentials.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
