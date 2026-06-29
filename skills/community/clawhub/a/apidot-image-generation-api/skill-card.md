## Description: <br>
Use APIDot for image generation API and image editing API workflows, including text-to-image API, image-to-image API, GPT Image 2 API, Nano Banana API, Nano Banana Pro API, Seedream API, Flux API, async task submission, polling, task status, and webhook integration based on APIDot docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this documentation-only skill to route APIDot image generation, editing, polling, and webhook questions to the right integration guidance and current APIDot references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDOT_API_KEY could be exposed if copied into browser code, logs, public repositories, screenshots, or chat output. <br>
Mitigation: Keep the key in server-side environment variables or a backend secret manager, and redact secrets from logs and generated guidance. <br>
Risk: Model-specific request fields, availability, or product behavior may change after release. <br>
Mitigation: Verify current APIDot docs and model pages before coding against model-specific fields or making product claims. <br>
Risk: Live image API calls can consume external service quota or process private prompts and image URLs. <br>
Mitigation: Make live API calls only after explicit user approval in a safe server-side environment, and avoid logging private prompts, source media URLs, final image URLs, and callback URLs. <br>


## Reference(s): <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Models](https://apidot.ai/models) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [GPT Image 2 Docs](https://apidot.ai/docs/gpt-image-2) <br>
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/apidot-image-generation-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable files or stored credentials are included in the release artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
