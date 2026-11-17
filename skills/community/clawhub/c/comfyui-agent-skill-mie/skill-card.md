## Description:

Runs registered ComfyUI workflows for image, video, music, and speech generation and supports reviewed imports of personal workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miemieeeee](https://clawhub.ai/user/miemieeeee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other ComfyUI users can direct an agent to run registered media-generation workflows on a local or trusted self-hosted server, check prerequisites, and import their own reviewed workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice cloning can enable impersonation without clear consent safeguards.

Mitigation: Use voice cloning only with clear permission from the voice owner and avoid impersonation.

Risk: Prompts and user-selected media may be sent to a ComfyUI server and generated outputs saved locally.

Mitigation: Connect only to a local or trusted server and review media and output locations before use.

Risk: Persisted server URLs may expose credentials or route media to untrusted hosts.

Mitigation: Do not save URLs containing credentials or pointing to untrusted hosts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/miemieeeee/skills/comfyui-agent-skill-mie)
- [Workflow selection and capabilities](artifact/references/workflows.md)
- [CLI usage and output handling](artifact/references/cli.md)
- [Workflow import and review](artifact/references/extension.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance, structured JSON results, and locally saved media]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media paths are returned in JSON; workflows require a local or trusted ComfyUI server.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
