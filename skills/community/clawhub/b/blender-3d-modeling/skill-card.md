## Description:

Blender 3D Modeling gives agents instructions for using AgentPMT-hosted Blender remote tool calls to render and convert 3D models, check and repair printability, slice models for printing, manage render tasks, and run scoped Blender Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to invoke hosted Blender workflows for game asset previews, e-commerce product views, 3D format conversion, printability checks and repairs, slicing, and custom Blender automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a hosted remote Blender provider and asks agents to trust mutable live schemas and remote instructions.

Mitigation: Install only when AgentPMT is trusted for the workflow, verify live schemas before production use, and prefer pinned or ClawHub-reviewed setup paths for account configuration.

Risk: Custom Blender Python execution can process uploaded models and create arbitrary output files within the hosted task context.

Mitigation: Keep scripts scoped to the requested task, avoid untrusted Blender Python, save only intended outputs, and do not include secrets, wallet material, signatures, or payment headers in prompts or logs.

Risk: Large renders, voxel remeshing, and script jobs can fail or queue because of GPU capacity, memory, grid-size, payload-size, or timeout limits.

Mitigation: Use documented limits and response warnings to select smaller renders, larger voxel sizes, or standard actions, then poll task status and retry only after correcting inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/blender-3d-modeling)
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/blender-3d-modeling)
- [Action schema](artifact/schema.md)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [text, markdown, code, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and response-handling instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote calls may return task IDs, JSON status responses, signed download URLs, rendered images or videos, converted model files, G-code, metadata, and Blender project files.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
