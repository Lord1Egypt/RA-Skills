## Description:

Use APIDot for Runway Gen-4.5 API workflows, including Runway Gen-4.5, text-to-video API, image-to-video API, cinematic motion, physics-aware video generation, duration planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Runway Gen-4.5 integration work through APIDot documentation, including text-to-video, image-guided video, async task submission, polling, and webhook planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if copied into chat, frontend code, logs, public repositories, screenshots, or generated examples.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager and avoid echoing credentials in generated guidance.

Risk: Runway Gen-4.5 API fields, availability, limits, and commercial terms may change outside the static skill artifact.

Mitigation: Verify current APIDot docs and model pages before preparing live API requests or making product claims.

Risk: Live API calls may submit prompts, media URLs, callback URLs, or generated video URLs to an external service.

Mitigation: Make live calls only from a safe server-side environment after explicit user request, and avoid logging private prompts, media URLs, callback URLs, API keys, or generated video URLs.

## Reference(s):

- [APIDot Runway Gen-4.5 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [Runway Gen-4.5 Model Page](https://apidot.ai/models/runway-gen-4-5)
- [Runway Gen-4.5 API Docs](https://apidot.ai/docs/runway-gen-4-5)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with optional code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no executable files, bundled clients, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
