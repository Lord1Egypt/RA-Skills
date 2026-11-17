## Description:

Run ComfyUI workflows from AI agents through a CLI that can discover workflows, manage dependencies, execute jobs across servers, and track results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangyuchuh](https://clawhub.ai/user/huangyuchuh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect Claude Code, OpenClaw, Codex, or another shell-capable agent to local ComfyUI workflows for image generation, workflow import, dependency checks, and multi-server execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Web UI exposes powerful unauthenticated controls for credentials, server requests, updates, and dependency installation.

Mitigation: Run it only on trusted machines, keep it bound to loopback, and do not expose it over a network.

Risk: Dependency installation and update flows can introduce code or configuration from external repositories.

Mitigation: Review repository URLs before installation and use isolated ComfyUI and Python environments.

Risk: Stored API keys or credentials may be sensitive until authentication and secret handling are improved.

Mitigation: Avoid storing high-value tokens and limit use to trusted local environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huangyuchuh/skills/comfyui-skill-openclaw)
- [Getting Started](docs/getting-started.md)
- [Architecture](docs/architecture.md)
- [Workflow Import Reference](references/workflow-import.md)
- [ComfyUI Native Local Routes](docs/comfyui-native-routes.md)
- [ComfyUI Server Overview](https://docs.comfy.org/development/comfyui-server/comms_overview)
- [ComfyUI Server Routes](https://docs.comfy.org/development/comfyui-server/comms_routes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return structured JSON status and local output file references from ComfyUI runs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
