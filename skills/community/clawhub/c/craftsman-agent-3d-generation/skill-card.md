## Description: <br>
Turn prompts or ideas into 3D assembly and build plans for LEGO or Minecraft using the Craftsman Agent API through OneKey Gateway or a local server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate LEGO or Minecraft build plans, part inventories, and step-by-step assembly image outputs from prompts or reference image URLs. It also helps agents wire Python or TypeScript clients to the hosted Craftsman Agent endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image URLs, and API keys are sent to the external DeepNLP/OneKey Gateway service. <br>
Mitigation: Use the skill only with prompts and image links approved for that service, avoid private designs or internal URLs, and set a scoped DEEPNLP_ONEKEY_ROUTER_ACCESS value. <br>
Risk: If no API key is configured, the helper scripts still contact the external service using a bundled shared demo key. <br>
Mitigation: Configure your own DEEPNLP_ONEKEY_ROUTER_ACCESS key before running the scripts, or review and modify the fallback behavior before deployment. <br>


## Reference(s): <br>
- [Craftsman Agent skill page](https://clawhub.ai/ai-hub-admin/craftsman-agent-3d-generation) <br>
- [Craftsman Agent API endpoint](https://agent.deepnlp.org/agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated build-plan responses may include overall image URLs, inventory lists, inventory image URLs, and ordered assembly-step image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
