## Description: <br>
Creates 3D models from source images or text prompts, refines text-generated drafts into textured assets, and retrieves task status and completed model download URLs through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agent workflows use this skill to submit image-to-3D or text-to-3D generation jobs, refine drafts, poll status, and retrieve downloadable 3D assets for prototyping, product visualization, games, AR, VR, or ecommerce. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: 3D prompts, source images, texture images, and related asset details are sent to the external AgentPMT service. <br>
Mitigation: Submit only content you have permission to share, and avoid private, regulated, copyrighted, client-owned, or proprietary material unless AgentPMT handling, billing, and policy terms are approved. <br>
Risk: Account secrets, payment headers, wallet keys, or similar credentials could be exposed if included in prompts or logs during setup or tool use. <br>
Mitigation: Use the referenced setup skill for credential handling and keep secrets out of prompts, logs, examples, and task parameters. <br>
Risk: Generated 3D tasks are asynchronous and completed download links expire after the service retention window. <br>
Mitigation: Poll task status, verify returned assets before relying on them, and retrieve completed model files promptly. <br>


## Reference(s): <br>
- [Action schema](schema.md) <br>
- [AgentPMT marketplace product page](https://www.agentpmt.com/marketplace/create-3d-model-from-image) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/create-3d-model-from-image) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, JSON, Files] <br>
**Output Format:** [Markdown instructions with JSON request examples; remote calls return JSON task metadata and model download URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Asynchronous generation; paid credit actions for creation and refinement; completed assets may include GLB, FBX, OBJ, and USDZ links that expire after the retention window.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
