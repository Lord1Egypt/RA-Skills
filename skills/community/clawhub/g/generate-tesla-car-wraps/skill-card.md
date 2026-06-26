## Description: <br>
Call Craftsman Agent API OneKey Router to generate Tesla Car Wrap Images and Paints that will display on 3D screen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can generate Tesla vehicle wrap concepts by sending text prompts and optional reference image URLs to the Craftsman Agent OneKey Router. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image URLs, and API-authenticated requests are sent to a third-party image-generation service. <br>
Mitigation: Use only approved prompts and image URLs, avoid sensitive or proprietary content, and confirm that third-party processing is acceptable for the use case. <br>
Risk: The skill requires an API key in DEEPNLP_ONEKEY_ROUTER_ACCESS. <br>
Mitigation: Use a revocable key, keep it out of logs and shared files, and rotate it if exposure is suspected. <br>
Risk: The skill documentation suggests global package installation for dependencies. <br>
Mitigation: Install dependencies in an isolated environment when operating in sensitive or controlled systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/generate-tesla-car-wraps) <br>
- [DeepNLP Workspace keys](https://www.deepnlp.org/workspace/keys) <br>
- [Craftsman Agent OneKey Router endpoint](https://agent.deepnlp.org/agent_router) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions] <br>
**Output Format:** [JSON responses and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated responses may include image URLs returned by the third-party service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
