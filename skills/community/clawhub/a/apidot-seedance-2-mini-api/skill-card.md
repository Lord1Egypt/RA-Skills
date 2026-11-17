## Description:

Use APIDot for Seedance 2.0 Mini API workflows, including low-cost short video generation, text-to-video, first and last frame image-to-video, reference image/video/audio workflows, 480p, 720p, task_id, polling, webhooks, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external builders use this skill to route APIDot Seedance 2.0 Mini integration work to the right docs, model pages, async task flow, polling, webhook, and credential-handling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys, prompts, media URLs, generated video URLs, callback URLs, task IDs, and customer data can expose sensitive information if handled in client code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep API keys in server-side environment variables or a backend secret manager, avoid logging sensitive values, and treat prompts, media URLs, callback URLs, generated video URLs, and task IDs as sensitive unless the user explicitly says they can be shared.

Risk: Live APIDot calls may submit sensitive prompts or media to an external API when a user expected documentation-only guidance.

Mitigation: Use the skill as documentation guidance by default and make live APIDot calls only when the user intentionally requests them in a safe server-side environment.

Risk: Model request fields, limits, availability, and commercial terms may change over time.

Mitigation: Use the current APIDot docs and model pages as the source of truth before preparing payloads or making product claims.

## Reference(s):

- [Local API reference](references/api.md)
- [APIDot documentation](https://apidot.ai/docs)
- [APIDot Seedance 2.0 Mini model page](https://apidot.ai/models/seedance-2-mini)
- [APIDot Seedance 2.0 Mini API docs](https://apidot.ai/docs/seedance-2-mini)
- [APIDot quickstart](https://apidot.ai/docs/quickstart)
- [APIDot webhooks](https://apidot.ai/docs/webhooks)
- [APIDot examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with documentation links and integration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; live API calls require an explicitly requested server-side environment.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
