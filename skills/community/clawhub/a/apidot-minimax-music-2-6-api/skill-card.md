## Description:

Use APIDot for MiniMax Music 2.6 API workflows, including AI music generation, lyrics, instrumentals, audio export planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route MiniMax Music 2.6 integration work through APIDot documentation, plan async task submission and polling, and handle webhook-based audio delivery. It supports agent guidance for API request planning while keeping credentials and live calls outside the skill artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys or private generation data could be exposed if copied into client code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager, and avoid logging API keys, private prompts, callback URLs, or generated audio URLs.

Risk: Model request fields, availability, pricing, or commercial terms may change outside the skill artifact.

Mitigation: Verify current APIDot docs and model pages before implementing payloads, limits, or product assumptions.

Risk: Async media jobs can fail, outlive a browser session, or deliver duplicate webhook callbacks.

Mitigation: Persist task_id and request metadata, poll for local testing, use callback_url for production workflows, retry transient failures with backoff, and make webhook handlers idempotent.

## Reference(s):

- [Local APIDot MiniMax Music 2.6 reference](references/api.md)
- [APIDot documentation](https://apidot.ai/docs)
- [MiniMax Music 2.6 model page](https://apidot.ai/models/minimax-music-2-6)
- [MiniMax Music 2.6 API docs](https://apidot.ai/docs/minimax-music-2-6)
- [APIDot quickstart](https://apidot.ai/docs/quickstart)
- [APIDot webhooks](https://apidot.ai/docs/webhooks)
- [APIDot examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with API integration notes and optional code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no bundled execution or automatic network calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
