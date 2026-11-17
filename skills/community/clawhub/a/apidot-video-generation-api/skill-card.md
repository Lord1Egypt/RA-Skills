## Description:

Use APIDot for video generation API workflows, including text-to-video API, image-to-video API, reference image video, Veo 3.1 API, Seedance 2 API, Sora API, Kling API, async task submission, polling, task status, and webhook integration based on APIDot docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route APIDot video generation questions to current docs, examples, and async integration guidance for text-to-video, image-to-video, polling, and webhook workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY may be exposed if copied into browser code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager and avoid displaying or logging it.

Risk: APIDot examples or model-specific fields may be stale or unsuitable for the user's environment.

Mitigation: Review the current APIDot documentation and example code before running it.

Risk: Live API calls can use third-party service resources and may process user prompts, media, or callback URLs.

Mitigation: Make live API calls only when the user explicitly asks and provides a safe server-side environment.

## Reference(s):

- [APIDot API Docs](https://apidot.ai/docs)
- [APIDot Models](https://apidot.ai/models)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Veo 3.1 Docs](https://apidot.ai/docs/veo-3-1)
- [APIDot Video Examples](https://github.com/APIDotAI/apidot-examples#video-models)
- [APIDot Veo 3.1 Examples](https://github.com/APIDotAI/veo-3.1-api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with links and optional code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no bundled executable behavior, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
