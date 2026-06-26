## Description: <br>
Turn prompts or ideas into 3D assembly/build plans such as LEGO Minecraft via the Craftsman Agent API, using OneKey Gateway or a local server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Hub-Admin](https://clawhub.ai/user/AI-Hub-Admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to generate LEGO or Minecraft build plans from prompts or reference image URLs. It helps produce part inventories, multi-angle assembly images, and step-by-step build guide data through the Craftsman Agent endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference image URLs are sent to an external Craftsman/OneKey service. <br>
Mitigation: Use the skill only with data suitable for that provider, and avoid sending private prompts, proprietary designs, or private image URLs unless the provider is trusted. <br>
Risk: The scripts can fall back to a bundled demo API key when a user key is not configured. <br>
Mitigation: Set a scoped DEEPNLP_ONEKEY_ROUTER_ACCESS key for real use, and treat demo-key results as limited demonstrations. <br>
Risk: The remote API is described as paid and may have billing or privacy terms outside the skill artifact. <br>
Mitigation: Review the provider's billing and privacy terms before commercial use. <br>


## Reference(s): <br>
- [Craftsman Agent ClawHub page](https://clawhub.ai/AI-Hub-Admin/craftsman-agent) <br>
- [Craftsman Agent API endpoint](https://agent.deepnlp.org/agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [API responses may include image URLs, part inventories, and ordered assembly-step image references.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
