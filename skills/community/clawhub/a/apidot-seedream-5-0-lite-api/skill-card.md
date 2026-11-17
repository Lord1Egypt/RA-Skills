## Description:

Routes agents to APIDot Seedream 5.0 Lite documentation and integration guidance for image generation, image editing, reference-guided workflows, async task handling, polling, task status, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find the right APIDot Seedream 5.0 Lite documentation path and plan image generation or editing integrations without inventing model-specific API details. It is useful for async task submission, task_id persistence, polling, webhook delivery, and safe API key handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY, private prompts, image URLs, generated image URLs, or callback URLs could be exposed during integration work.

Mitigation: Keep APIDOT_API_KEY in server-side secret storage, never place it in browser code or public repos, and avoid logging prompts, image URLs, generated image URLs, callback URLs, or keys.

Risk: Outdated or guessed Seedream 5.0 Lite request fields could produce invalid payloads or misleading integration guidance.

Mitigation: Verify current model-specific fields, limits, availability, and commercial terms in APIDot's live docs before making real API calls.

## Reference(s):

- [APIDot Seedream 5.0 Lite Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [Seedream 5.0 Lite Model Page](https://apidot.ai/models/seedream-5-0-lite)
- [Seedream 5.0 Lite API Docs](https://apidot.ai/docs/seedream-5-0-lite)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-seedream-5-0-lite-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with documentation links and optional code or configuration snippets when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; does not execute API calls, make network requests, or store credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
