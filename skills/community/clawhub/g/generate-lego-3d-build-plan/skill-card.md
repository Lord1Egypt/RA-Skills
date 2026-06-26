## Description: <br>
Call Craftsman Agent API OneKey Router to generate a LEGO 3D step-by-step instruction build plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to call the Craftsman Agent API and generate a LEGO build plan from a text prompt, optional reference image URLs, and a selected generation mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and the API key are sent to the DeepNLP/Craftsman remote API. <br>
Mitigation: Use a dedicated or scoped API key when available and avoid sending secrets or confidential details in prompts or image URLs. <br>
Risk: The recommended onekey CLI is separate from the bundled Python and TypeScript REST scripts. <br>
Mitigation: Verify the onekey CLI before using that path, or use the provided REST scripts after reviewing their behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ai-hub-admin/generate-lego-3d-build-plan) <br>
- [DeepNLP Workspace keys](https://www.deepnlp.org/workspace/keys) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown instructions with shell examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPNLP_ONEKEY_ROUTER_ACCESS; sends the prompt, optional image URLs, and mode to a remote API.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
