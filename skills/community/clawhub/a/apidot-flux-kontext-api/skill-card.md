## Description:

Routes agents to APIDot Flux Kontext documentation and integration guidance for image generation, context-aware editing, async task handling, polling, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find APIDot Flux Kontext docs, plan image generation or editing workflows, and implement async task submission, polling, and webhook delivery without embedding credentials in the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys or private media details could be exposed in frontend code, logs, screenshots, public repos, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager, and avoid logging API keys, private prompts, private image URLs, generated image URLs, or callback URLs.

Risk: Live API calls could be made unintentionally while a user is only asking for documentation or planning help.

Mitigation: Treat the skill as documentation guidance and make live APIDot calls only when the user explicitly asks and provides a safe server-side environment.

Risk: Model fields, limits, availability, or commercial terms may become stale if copied from memory or from another image model family.

Mitigation: Use current APIDot docs and model pages as the source of truth before preparing payloads or making product claims.

Risk: Async image workflows may lose task state or create duplicate visible results when polling, retries, or webhook callbacks are handled incorrectly.

Mitigation: Persist task_id, selected model, user ID, source media references, request status, and final image URLs together; make webhook handlers idempotent and retry only transient network failures with backoff.

## Reference(s):

- [APIDot Flux Kontext Reference](references/api.md)
- [APIDot Documentation](https://apidot.ai/docs)
- [APIDot Flux Kontext Model Page](https://apidot.ai/models/flux-kontext)
- [APIDot Flux Kontext API Docs](https://apidot.ai/docs/flux-kontext)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with optional code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill with no bundled clients, executable automation, stored credentials, or automatic network calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
