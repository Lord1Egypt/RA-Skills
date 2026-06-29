## Description: <br>
Use APIDot for Tripo H3.1 3D API workflows, including Tripo H3.1 API, text-to-3D API, image-to-3D API, multiview-to-3D API, 3D asset generation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan APIDot Tripo H3.1 3D integrations for text-to-3D, image-to-3D, multiview-to-3D, async polling, and webhook workflows. It routes users to current APIDot documentation and local non-executable reference notes before preparing implementation details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API credentials can be exposed if copied into frontend code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Store APIDOT_API_KEY only in server-side environment variables or a backend secret manager and avoid echoing it in generated guidance. <br>
Risk: Outdated or guessed API fields can cause failed Tripo H3.1 requests or misleading implementation guidance. <br>
Mitigation: Use the current APIDot model page and docs for model-specific payload fields, supported modes, limits, and commercial terms. <br>
Risk: Async job handling can lose or duplicate generated assets if task IDs, polling, or webhook callbacks are not handled carefully. <br>
Mitigation: Persist task_id and related request metadata, store final asset URLs only after terminal success, and make webhook handlers idempotent. <br>


## Reference(s): <br>
- [APIDot Tripo H3.1 Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Tripo H3.1 Model Page](https://apidot.ai/models/tripo-h31-3d) <br>
- [APIDot Tripo H3.1 3D Docs](https://apidot.ai/docs/tripo-h31-3d) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown with implementation guidance and links to API documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference APIDOT_API_KEY as a server-side environment variable; the artifact contains no executable files, bundled clients, stored credentials, or automatic network calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
