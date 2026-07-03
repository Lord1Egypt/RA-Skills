## Description: <br>
Use APIDot for Seedream 4 API workflows, including 4K image generation, image editing, image-to-image planning, reference image generation, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this documentation-only skill to route APIDot Seedream 4 integration work, including image generation, editing, async task polling, and webhook planning, to the right APIDot references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDOT_API_KEY or private image data could be exposed when users adapt the guidance for real API calls. <br>
Mitigation: Keep APIDOT_API_KEY in server-side secrets only, avoid browser bundles and logs, and avoid logging prompts, private image URLs, generated image URLs, or callback URLs. <br>
Risk: APIDot model fields, availability, limits, or commercial terms may change after this documentation-only release. <br>
Mitigation: Verify the current APIDot docs and model page before preparing request payloads or sending live requests. <br>


## Reference(s): <br>
- [APIDot documentation](https://apidot.ai/docs) <br>
- [APIDot Seedream 4 model page](https://apidot.ai/models/seedream-4) <br>
- [APIDot Seedream 4 API docs](https://apidot.ai/docs/seedream-4) <br>
- [APIDot quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot examples](https://github.com/APIDotAI/apidot-examples) <br>
- [APIDot Seedream 4 Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code snippets, shell commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; it does not execute network requests, store credentials, or bundle API clients.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
