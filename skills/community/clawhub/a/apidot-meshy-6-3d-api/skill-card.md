## Description: <br>
Use APIDot for Meshy 6 3D API workflows, including Meshy 6 API, text-to-3D API, image-to-3D API, multi-image-to-3D API, 3D asset generation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route Meshy 6 3D API integration work through APIDot documentation, including text-to-3D, image-to-3D, multi-image-to-3D, async task polling, and webhook workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDOT_API_KEY exposure could leak credentials if copied into browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager and avoid logging secrets or private asset data. <br>
Risk: Live APIDot requests may consume provider credits or create external generated assets. <br>
Mitigation: Confirm live API calls with the user and use a safe server-side environment before making requests. <br>
Risk: Stale or guessed API payload fields could cause incorrect integration guidance. <br>
Mitigation: Use current APIDot docs and model pages for model-specific fields, limits, availability, and commercial terms. <br>


## Reference(s): <br>
- [APIDot Meshy 6 Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Meshy 6 Model Page](https://apidot.ai/models/meshy-6-3d) <br>
- [APIDot Meshy 6 3D Docs](https://apidot.ai/docs/meshy-6-3d) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with optional code and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; includes no executable files, automatic network calls, bundled API clients, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
