## Description:

Use APIDot for Seedance 2 API workflows, including seedance-2-fast, text-to-video API, image-to-video API, native audio video generation, reference image video, reference video, reference audio, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and implement APIDot Seedance 2 video generation workflows, including request routing, async task handling, polling, webhook delivery, and optional reviewed task submission from a server-side shell.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional submit script sends prompts, media URLs, callback URLs, and request data to APIDot and may incur account usage or costs.

Mitigation: Run the script only after reviewing the JSON payload, confirming the APIDot account context, and choosing to make a live API request.

Risk: APIDOT_API_KEY is a credential used for live APIDot API calls.

Mitigation: Keep the key in a server-side environment or secret manager and avoid placing it in browser code, payload files, logs, screenshots, repositories, or chat output.

Risk: Generated workflow behavior depends on current APIDot model fields, limits, and availability.

Mitigation: Use the current APIDot docs and model page before preparing or submitting Seedance 2 payloads.

## Reference(s):

- [APIDot Seedance 2 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [Seedance 2 API Docs](https://apidot.ai/docs/seedance-2)
- [Seedance 2 Model Page](https://apidot.ai/models/seedance-2)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [Seedance 2 Examples](https://github.com/APIDotAI/seedance-2-api)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with optional shell command usage and JSON payload handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require curl and a server-side APIDOT_API_KEY when the optional submit script is explicitly used.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
