## Description:

Use APIDot for Seedream 4 API workflows, including 4K image generation, image editing, image-to-image planning, reference image generation, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan APIDot Seedream 4 integrations for image generation, image editing, reference-guided workflows, async task polling, and webhook delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY could be exposed if copied into browser code, public logs, repositories, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager, and avoid logging credentials or private request data.

Risk: Model request fields, limits, availability, and commercial terms may change outside this documentation-only skill.

Mitigation: Use the live APIDot docs and model page as the source of truth before preparing payloads or making product commitments.

Risk: Unintentional live API calls could consume account quota or submit private prompts and image URLs.

Mitigation: Make live APIDot calls only when the user explicitly asks and a safe server-side environment is available.

## Reference(s):

- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Seedream 4 Model Page](https://apidot.ai/models/seedream-4)
- [APIDot Seedream 4 API Docs](https://apidot.ai/docs/seedream-4)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [APIDot Seedream 4 Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-seedream-4-api)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown with integration guidance, API planning notes, and code or configuration snippets when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no executable files or automatic network calls are included.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
