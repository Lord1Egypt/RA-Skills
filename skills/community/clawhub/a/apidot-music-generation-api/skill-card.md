## Description:

Use APIDot for music generation API workflows, including text-to-music API, song generation API, Generate Music API, MiniMax Music 2.6 API, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route APIDot music-generation questions to current docs, examples, and async integration guidance for task submission, polling, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real APIDot API use can expose API keys, prompts, generated audio URLs, or callback URLs if handled in browser code, logs, screenshots, public repos, or chat output.

Mitigation: Keep APIDOT_API_KEY server-side, use environment variables or a backend secret manager, and avoid logging private prompts, generated URLs, or callback URLs.

Risk: Live API calls may affect a user's account or workflow if made without explicit approval.

Mitigation: Make live APIDot API calls only when the user explicitly asks and provides a safe server-side environment.

Risk: Model-specific request fields, pricing, availability, reliability, refund behavior, or comparisons can become inaccurate if invented from memory.

Mitigation: Use current APIDot docs and model pages for model-specific details and do not infer unsupported claims.

## Reference(s):

- [APIDot API Docs](https://apidot.ai/docs)
- [APIDot Music Models](https://apidot.ai/models/music)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [Generate Music Docs](https://apidot.ai/docs/generate-music)
- [MiniMax Music 2.6 Docs](https://apidot.ai/docs/minimax-music-2-6)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with API integration notes, links, and copyable code or configuration when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no executable files, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
