## Description:

Use APIDot for Kling Avatar 2.0 API workflows, including talking avatar video, image-and-audio-to-video, Standard and Pro variants, avatar performance direction, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan APIDot Kling Avatar 2.0 integrations for talking-avatar video generation from one reference image and one speech audio track. It helps route users to current APIDot documentation, select Standard or Pro variants, and design async task polling or webhook handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY server-side in environment variables or a backend secret manager, and avoid logging credentials.

Risk: Private media URLs, callback URLs, prompts, or generated video URLs could reveal sensitive user content.

Mitigation: Avoid logging private media or generated URLs, and make live API calls only from an environment the user controls.

Risk: Outdated or guessed request fields, model availability, media limits, or commercial terms could cause incorrect integrations.

Mitigation: Use the current APIDot docs and model pages as the source of truth for payload fields, limits, variants, and product details.

## Reference(s):

- [Local APIDot Kling Avatar 2.0 Reference](references/api.md)
- [APIDot Kling Avatar 2.0 API Docs](https://apidot.ai/docs/kling-avatar-2-0)
- [APIDot Kling Avatar 2.0 Model Page](https://apidot.ai/models/kling-avatar-2-0)
- [APIDot API Docs](https://apidot.ai/docs)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-kling-avatar-2-0-api)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with optional code snippets and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no bundled executable files, install-time automation, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
