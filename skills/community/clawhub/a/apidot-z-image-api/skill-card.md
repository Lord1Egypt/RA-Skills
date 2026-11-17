## Description:

Use APIDot docs and workflow guidance to plan Z-Image text-to-image integrations, including prompt generation, async task handling, polling, webhooks, and API-key hygiene.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route APIDot Z-Image questions to the right docs and plan prompt-based image generation integrations with async submission, task status polling, and webhook delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed through browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager, and never include it in frontend bundles or user-visible output.

Risk: Generated image URLs, callback URLs, or private prompts could be logged or stored more broadly than intended.

Mitigation: Avoid logging private prompts, callback URLs, API keys, and generated image URLs; persist only the task metadata and results needed for the workflow.

Risk: Stale or guessed Z-Image request fields could lead to incorrect integration guidance.

Mitigation: Check live APIDot docs and model pages for current request fields, limits, availability, and commercial terms before preparing copyable payloads.

Risk: Async image jobs may lose state or duplicate visible results if task IDs and webhook callbacks are handled inconsistently.

Mitigation: Persist task_id with selected model, prompt metadata, status, and final image URLs, and make webhook handlers idempotent.

## Reference(s):

- [Local APIDot Z-Image Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Z-Image Model Page](https://apidot.ai/models/z-image)
- [APIDot Z-Image API Docs](https://apidot.ai/docs/z-image)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration guidance]

**Output Format:** [Markdown guidance with links and optional code-oriented implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable files, bundled clients, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
