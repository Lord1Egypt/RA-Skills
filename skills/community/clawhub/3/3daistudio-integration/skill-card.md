## Description:

Convert images and text prompts to 3D models (.glb) using the 3D AI Studio API. Supports TRELLIS.2, Hunyuan Rapid, and Hunyuan Pro models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whale-professor](https://clawhub.ai/user/whale-professor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, artists, and automation agents use this skill to turn image inputs or text prompts into downloadable .glb 3D model files through the 3D AI Studio API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-run generation commands can spend paid 3D AI Studio account credits.

Mitigation: Require explicit approval before each paid generation and check the requested model, options, and estimated credit cost before execution.

Risk: The skill requires a 3D AI Studio API key.

Mitigation: Store the key only in the THREE_D_AI_STUDIO_API_KEY environment variable and limit use to agents and workspaces trusted with that account.

Risk: Downloaded result URLs are provider-supplied and are not constrained by host, size, or file-type checks in the artifact.

Mitigation: Use a limited-output directory and review or harden downloads to require HTTPS, trusted 3D AI Studio or CDN hosts, and size and format limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whale-professor/skills/3daistudio-integration)
- [3D AI Studio homepage](https://www.3daistudio.com)
- [3D AI Studio API dashboard](https://www.3daistudio.com/Platform/API)
- [3D AI Studio API documentation](https://www.3daistudio.com/Platform/API/Documentation)

## Skill Output:

**Output Type(s):** [Files, Shell commands, API Calls, Configuration instructions]

**Output Format:** [GLB model files with terminal text and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires THREE_D_AI_STUDIO_API_KEY and a funded 3D AI Studio account; generation jobs are asynchronous and may spend account credits.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
