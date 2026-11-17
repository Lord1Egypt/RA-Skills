## Description:

Use APIDot for Generate Music API workflows, including prompt-to-song generation, instrumental generation, vocal music planning, async task submission, task_id handling, music detail polling, callback_url planning, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building APIDot Generate Music integrations use this skill to route questions to the right APIDot documentation and plan asynchronous task submission, polling, callback_url, webhook, and credential-handling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY or user music-generation data could be exposed if copied into frontend code, logs, screenshots, chat output, or public repositories.

Mitigation: Keep the API key in server-side secrets and avoid logging private prompts, webhook payloads, callback URLs, generated audio links, or API credentials.

Risk: APIDot model fields, limits, pricing, or availability may change after the skill release.

Mitigation: Verify current APIDot docs and model pages before preparing request payloads or making product claims.

Risk: Asynchronous music jobs can be mishandled if task IDs, terminal states, retries, or webhook duplicates are not persisted consistently.

Mitigation: Persist task_id, selected model, status, prompt metadata, user ID, and final audio URLs together; make callback_url and webhook handlers idempotent.

## Reference(s):

- [APIDot Generate Music Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [Generate Music Docs](https://apidot.ai/docs/generate-music)
- [Generate Music Model Page](https://apidot.ai/models/generate-music)
- [Music Detail Docs](https://apidot.ai/docs/music-detail)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with links and concise implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable behavior, automatic network calls, bundled API clients, or stored credentials.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
