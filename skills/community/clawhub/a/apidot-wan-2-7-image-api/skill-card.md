## Description: <br>
Routes Wan 2.7 Image integration questions to APIDot documentation, model pages, request-planning notes, async polling guidance, webhook guidance, and API-key handling guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan APIDot Wan 2.7 Image integrations, choose the right documentation path, and handle asynchronous image generation, editing, polling, and webhook workflows without embedding executable clients in the skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys, prompts, private image URLs, callback URLs, or generated outputs could be exposed if copied into client code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY server-side, use backend secret storage, and avoid logging or publicly sharing prompts, private media URLs, callback URLs, API keys, or generated outputs. <br>
Risk: Model-specific API fields, availability, limits, commercial terms, or request modes may change outside the skill. <br>
Mitigation: Use current APIDot documentation and model pages before preparing payloads or making claims about supported fields, availability, limits, or terms. <br>
Risk: Live APIDot calls may submit private prompts or media to an external service unexpectedly. <br>
Mitigation: Do not make live API calls unless the user explicitly asks and provides a safe server-side environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiehao71727/skills/apidot-wan-2-7-image-api) <br>
- [APIDot documentation](https://apidot.ai/docs) <br>
- [APIDot Wan 2.7 Image model page](https://apidot.ai/models/wan-2-7-image) <br>
- [APIDot Wan 2.7 Image docs](https://apidot.ai/docs/wan-2-7-image) <br>
- [APIDot quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with documentation links and integration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; no executable files, shell automation, bundled API client, network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
