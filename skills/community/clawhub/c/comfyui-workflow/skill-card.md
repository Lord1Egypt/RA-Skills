## Description:

Universal ComfyUI workflow executor with 33+ workflow templates that lets agents inspect inputs and outputs automatically and run workflows against local ComfyUI, Windows Portable via WSL, or remote servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiqiliu2](https://clawhub.ai/user/yiqiliu2)

### License/Terms of Use:

MIT

## Use Case:

Developers and creative workflow operators use this skill to inspect, configure, and run ComfyUI image, video, audio, and editing workflows through a consistent command-line interface. It helps agents translate user requests into workflow parameters, submit jobs to a running ComfyUI server, and collect generated outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote ComfyUI use can send prompts, media, and authentication tokens over plaintext HTTP or WebSocket connections.

Mitigation: Prefer loopback-only ComfyUI or a TLS-protected remote endpoint, and avoid sending tokens over remote plaintext connections.

Risk: Persistent workflow and model cache files can record local setup details such as model names, paths, and workflow capabilities.

Mitigation: Review or disable persistent caches before allowing an agent to scan local model directories or store environment-specific details.

Risk: The skill can read selected local media files and write generated outputs through the configured ComfyUI workflow.

Mitigation: Run the skill in a dedicated environment with limited file access and review selected input and output directories before execution.

Risk: Voice-cloning or identity-like generation capabilities may be misused without consent.

Mitigation: Use voice-cloning and identity-preserving generation only with clear consent and appropriate review of the requested use.

## Reference(s):

- [ComfyUI Workflow Skill on ClawHub](https://clawhub.ai/yiqiliu2/skills/comfyui-workflow)
- [README](README.md)
- [Practical Guide](PRACTICAL_GUIDE.md)
- [Workflows Summary](WORKFLOWS_SUMMARY.md)
- [Models Inventory](MODELS_INVENTORY.md)
- [Architecture](references/architecture.md)
- [Maintenance](references/maintenance.md)
- [Prompting Guide](references/prompting-guide.md)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI-Easy-Use](https://github.com/yolain/ComfyUI-Easy-Use)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell and Python code blocks; workflow execution saves generated media files to the configured output directory.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running ComfyUI server and configured workflow paths; may read selected input media and write generated image, video, or audio outputs.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
