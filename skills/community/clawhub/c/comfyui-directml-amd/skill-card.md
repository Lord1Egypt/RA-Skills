## Description:

Sets up and optimizes ComfyUI on AMD GPUs with DirectML on Windows, including setup guidance, compatibility fixes, model recommendations, benchmarks, and configuration examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vilda007](https://clawhub.ai/user/vilda007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and local generative-media users use this skill to run and troubleshoot ComfyUI on Windows systems with AMD Radeon GPUs through DirectML. It helps configure the environment, apply DirectML compatibility fixes, choose model settings for available VRAM, and connect ComfyUI to OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a local patch script that modifies ComfyUI's comfy/model_patcher.py file.

Mitigation: Inspect apply-directml-fixes.py before running it, confirm it targets the intended ComfyUI directory, and keep a separate backup or version-control copy of comfy/model_patcher.py.

Risk: Model downloads and Python package installs may change over time or resolve to unexpected artifacts.

Mitigation: Prefer pinned package versions and verify downloaded model checksums when possible before using them in the local ComfyUI environment.

## Reference(s):

- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [DirectML Documentation](https://learn.microsoft.com/en-us/windows/ai/directml/)
- [AMD ROCm Blogs](https://rocm.blogs.amd.com/)
- [CivitAI Models](https://civitai.com/)
- [ClawHub Skill Page](https://clawhub.ai/vilda007/skills/comfyui-directml-amd)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, PowerShell, JSON, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local setup steps, compatibility patch guidance, model recommendations, benchmark expectations, and OpenClaw configuration examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
