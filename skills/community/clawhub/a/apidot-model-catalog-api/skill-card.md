## Description: <br>
Use APIDot model catalog guidance to choose currently available APIDot image, video, chat, music, and 3D model pages, avoid offline model routes, prevent duplicate skill selection, and route users to the right APIDot docs and model-specific skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route APIDot model-selection questions to the right live model catalog page, category skill, or model-specific skill while preserving API-key handling guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Store APIDOT_API_KEY only in server-side environment variables or an approved backend secret manager. <br>
Risk: Model availability, product details, pricing, or commercial terms may be misstated if the agent relies on stale or local draft information. <br>
Mitigation: Verify current details against APIDot model pages and docs before presenting availability or terms. <br>
Risk: Live API calls may be made in an unsafe context if the user has not explicitly requested them or provided a suitable server-side environment. <br>
Mitigation: Do not make live API calls unless the user explicitly asks and provides a safe server-side environment. <br>


## Reference(s): <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Model Catalog](https://apidot.ai/models) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-model-catalog-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with links, routing recommendations, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; no executable behavior, bundled API client, automatic network calls, or credential storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
