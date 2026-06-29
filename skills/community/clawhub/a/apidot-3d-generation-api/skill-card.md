## Description: <br>
Use APIDot for 3D generation API workflows, including text-to-3D API, image-to-3D API, multi-image-to-3D, Meshy 6 API, Tripo H3.1 API, Tripo P1 API, task_id handling, polling, task status, and webhook integration based on APIDot docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route APIDot 3D generation questions to current docs, examples, and async integration patterns for text-to-3D, image-to-3D, multi-image-to-3D, polling, and webhook workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys or private request data could be exposed in client code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a secret manager, and avoid logging prompts, private media URLs, callback URLs, generated asset links, or credentials. <br>
Risk: Live APIDot calls may use stale model details, pricing, or request fields. <br>
Mitigation: Review current APIDot docs, model pages, and pricing before making live calls, and make live calls only when the user explicitly asks from a safe server-side environment. <br>


## Reference(s): <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot 3D Models](https://apidot.ai/models/3d) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [Meshy 6 3D Docs](https://apidot.ai/docs/meshy-6-3d) <br>
- [Tripo H3.1 3D Docs](https://apidot.ai/docs/tripo-h31-3d) <br>
- [Tripo P1 3D Docs](https://apidot.ai/docs/tripo-p1-3d) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with optional code snippets and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable files, automatic network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
