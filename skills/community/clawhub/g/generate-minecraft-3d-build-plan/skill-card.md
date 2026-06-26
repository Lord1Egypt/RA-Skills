## Description: <br>
Call Craftsman Agent API OneKey Router to generate a Minecraft 3D scene build plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Minecraft creators use this skill to send text prompts and optional reference image URLs to the Craftsman Agent API and receive a generated Minecraft 3D scene build plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and optional image URLs to a remote Craftsman/DeepNLP API using a user-provided API key. <br>
Mitigation: Use it only with trusted data, avoid private prompts or image URLs, and keep DEEPNLP_ONEKEY_ROUTER_ACCESS secret. <br>
Risk: The artifact installs optional npm and Python packages for API access. <br>
Mitigation: Review and pin third-party package versions before installing in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/generate-minecraft-3d-build-plan) <br>
- [DeepNLP Workspace keys](https://www.deepnlp.org/workspace/keys) <br>
- [Craftsman Agent router endpoint](https://agent.deepnlp.org/agent_router) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with CLI, Python, and TypeScript examples; remote API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPNLP_ONEKEY_ROUTER_ACCESS and sends prompts and optional image URLs to a remote Craftsman/DeepNLP API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
