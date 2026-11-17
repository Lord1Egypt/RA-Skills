## Description:

Use APIDot for Hunyuan 3D 3.1 API workflows, including Hunyuan 3D Pro and Rapid variants, text-to-3D API, image-to-3D API, multi-view guidance, PBR output planning, geometry controls, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this documentation-only skill to plan APIDot Hunyuan 3D 3.1 integrations for text-to-3D, image-to-3D, async task polling, webhook delivery, and supported output controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys are real secrets and could be exposed if placed in browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY server-side in environment variables or a backend secret manager and avoid logging credentials or private asset URLs.

Risk: Live API calls may use paid or external services if made outside an intentional backend environment.

Mitigation: Only allow live API calls when the user explicitly requests them and provides a safe server-side environment.

Risk: Model variants, supported controls, limits, availability, and commercial terms can change in APIDot's live product documentation.

Mitigation: Use the current APIDot docs and model pages as the source of truth before preparing requests or advising on supported fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiehao71727/skills/apidot-hunyuan-3d-3-1-api)
- [APIDot Hunyuan 3D 3.1 docs](https://apidot.ai/docs/hunyuan-3d-3-1)
- [APIDot Hunyuan 3D 3.1 model page](https://apidot.ai/models/hunyuan-3d-3-1)
- [APIDot 3D models](https://apidot.ai/models/3d)
- [APIDot quickstart](https://apidot.ai/docs/quickstart)
- [APIDot webhooks](https://apidot.ai/docs/webhooks)
- [APIDot examples](https://github.com/APIDotAI/apidot-examples)
- [APIDot Hunyuan 3D 3.1 Reference](references/api.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with documentation links and integration planning notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable code, automation, credential storage, or automatic network calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
