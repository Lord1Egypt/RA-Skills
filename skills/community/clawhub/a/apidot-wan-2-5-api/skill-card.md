## Description:

Use APIDot for Wan 2.5 API workflows, including Alibaba Wan 2.5, text-to-video API, image-to-video API, optional audio text planning, short video generation, 480p 720p 1080p planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route Wan 2.5 API integration questions to APIDot documentation, model pages, async task guidance, polling, webhook, and API key handling notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys or private media details could be exposed if copied into client-side code, logs, repositories, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side secrets or environment variables and avoid logging API keys, private prompts, private media URLs, generated video URLs, or callback URLs.

Risk: Model fields, limits, pricing, and availability may change outside this documentation-only skill.

Mitigation: Use the live APIDot documentation and model page for current request fields, commercial terms, and product details before making real API calls.

Risk: Live APIDot calls may create external tasks or process user media when intentionally invoked.

Mitigation: Only make live API calls after explicit user approval and with a safe server-side environment; persist task_id, status, media references, and final URLs together.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiehao71727/skills/apidot-wan-2-5-api)
- [APIDot documentation](https://apidot.ai/docs)
- [APIDot Wan 2.5 model page](https://apidot.ai/models/wan-2-5)
- [APIDot Wan 2.5 API docs](https://apidot.ai/docs/wan-2-5)
- [APIDot quickstart](https://apidot.ai/docs/quickstart)
- [APIDot webhooks](https://apidot.ai/docs/webhooks)
- [APIDot examples](https://github.com/APIDotAI/apidot-examples)
- [APIDot Wan 2.5 Reference](references/api.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions, API Calls]

**Output Format:** [Markdown guidance with links, integration notes, and API workflow recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no executable files, bundled clients, stored credentials, or automatic network calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
