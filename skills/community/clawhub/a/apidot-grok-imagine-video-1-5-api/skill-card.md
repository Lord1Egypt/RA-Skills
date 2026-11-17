## Description:

Grok Imagine Video 1.5 API on APIDot for xAI image-to-video generation, reference image animation, prompt-guided motion, short video clips, duration planning, 480p 720p planning, async task submission, task_id handling, polling, webhooks, API key safety, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this documentation-only skill to route Grok Imagine Video 1.5 integration work to APIDot model pages, docs, async task guidance, polling, webhooks, and API-key handling notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or private media details could be exposed if copied into browser code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager, and avoid logging private prompts, private media URLs, generated video URLs, callback URLs, or API keys.

Risk: APIDot request fields, model availability, limits, or commercial terms may change after the skill release.

Mitigation: Verify the live APIDot docs and model page before making real API calls or publishing copyable request examples.

Risk: Webhook retries or duplicate callback delivery can create duplicate visible results in production workflows.

Mitigation: Persist task IDs and make webhook handlers idempotent before attaching generated videos to user-visible records.

## Reference(s):

- [APIDot Grok Imagine Video 1.5 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [Grok Imagine Video 1.5 Model Page](https://apidot.ai/models/grok-imagine-video-1-5)
- [Grok Imagine Video 1.5 API Docs](https://apidot.ai/docs/grok-imagine-video-1-5)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with links, planning notes, and copyable integration guidance when supported by current APIDot docs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable files, bundled clients, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
