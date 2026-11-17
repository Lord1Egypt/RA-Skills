## Description:

Use APIDot for Veo 3.1 API workflows, including Google Veo API, veo3.1-lite, veo3.1-fast, veo3.1-quality, text-to-video API, image-to-video API, reference image video, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan APIDot Veo 3.1 integrations, route users to current APIDot documentation, and optionally submit a reviewed video-generation payload from a trusted server-side shell.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY could be exposed if used in browser code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep the key in a server-side environment variable or backend secret manager and avoid printing or embedding it in payloads.

Risk: Prompts, source media URLs, generated video URLs, callback URLs, task details, and task IDs submitted through the helper are shared with APIDot.

Mitigation: Review each payload before submission and submit only data the user intends to share with APIDot.

Risk: The optional submit helper makes a live APIDot network request when explicitly invoked.

Mitigation: Run the helper only from a trusted server-side shell after reviewing the JSON payload and confirming curl and APIDOT_API_KEY are available.

Risk: Model-specific fields, availability, limits, or commercial terms may change outside this package.

Mitigation: Use the current APIDot docs and model page as the source of truth before preparing or submitting Veo 3.1 payloads.

## Reference(s):

- [APIDot Veo 3.1 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Veo 3.1 API Docs](https://apidot.ai/docs/veo-3-1)
- [APIDot Veo 3.1 Model Page](https://apidot.ai/models/veo-3-1)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Veo 3.1 Examples](https://github.com/APIDotAI/veo-3.1-api)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with links, JSON payload review guidance, and optional shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit an explicit user-run shell command for the bundled submit helper; live requests require APIDOT_API_KEY and curl.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
