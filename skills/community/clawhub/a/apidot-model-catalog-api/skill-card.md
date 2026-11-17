## Description:

Use APIDot model catalog guidance to choose currently available APIDot image, video, chat, music, and 3D model pages, avoid offline model routes, prevent duplicate skill selection, and route users to the right APIDot docs and model-specific skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route APIDot model-selection and integration questions to the right APIDot catalog page, documentation page, category skill, or model-specific skill while avoiding unavailable routes and unsupported claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY or private prompt, media, callback, transcript, or user data could be exposed if used in browser code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep APIDot API keys and private integration data in approved server-side environment variables, backend secret managers, and secure storage; avoid logging or displaying secrets.

Risk: Live API calls or storage of prompts and media data could occur in an environment that has not been approved for those operations.

Mitigation: Only make live API calls or persist prompts, media URLs, task IDs, transcripts, and user identifiers when the user explicitly requests it and provides an approved server-side environment.

Risk: Outdated or unsupported model routing could lead users to unavailable APIDot model pages or invented product details.

Mitigation: Use the current APIDot model catalog and model pages for availability and product details, and avoid inventing pricing, performance, reliability, benchmark, commercial-term, or competitor-comparison claims.

## Reference(s):

- [APIDot API Docs](https://apidot.ai/docs)
- [APIDot Model Catalog](https://apidot.ai/models)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-model-catalog-api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions]

**Output Format:** [Markdown guidance with links and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable files, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
