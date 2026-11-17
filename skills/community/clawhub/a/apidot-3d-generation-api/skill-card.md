## Description:

Use APIDot for 3D generation API workflows, including text-to-3D API, image-to-3D API, multi-image-to-3D, Meshy 6 API, Tripo H3.1 API, Tripo P1 API, task_id handling, polling, task status, and webhook integration based on APIDot docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find the right APIDot 3D generation docs, examples, and async integration pattern for text-to-3D, image-to-3D, multi-image-to-3D, polling, and webhook workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if placed in browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager, and avoid logging credentials or private asset URLs.

Risk: Model-specific request fields, pricing, or availability can change outside this documentation-only skill.

Mitigation: Verify live APIDot docs and model pages before making real API calls or committing integration behavior.

Risk: Async 3D jobs can create duplicate or stale assets if polling and webhook callbacks are not handled carefully.

Mitigation: Persist task_id and related request state, treat webhook handlers as idempotent, and store final asset URLs only after terminal success.

## Reference(s):

- [APIDot API Docs](https://apidot.ai/docs)
- [APIDot 3D Models](https://apidot.ai/models/3d)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [Meshy 6 3D Docs](https://apidot.ai/docs/meshy-6-3d)
- [Tripo H3.1 3D Docs](https://apidot.ai/docs/tripo-h31-3d)
- [Tripo P1 3D Docs](https://apidot.ai/docs/tripo-p1-3d)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-3d-generation-api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with links, integration guidance, and optional code or shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; it does not bundle executable behavior or make automatic network calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
