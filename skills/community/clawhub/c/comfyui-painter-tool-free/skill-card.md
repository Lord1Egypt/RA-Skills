## Description:

A local ComfyUI text-to-image helper that supports basic workflows, default model use, parameter tuning, and local image output for personal creative work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through local ComfyUI text-to-image setup, parameter selection, command execution, and saving generated images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activation language and execution scope are broader than the stated local ComfyUI image-generation purpose.

Mitigation: Review the skill before installing and use it only for local ComfyUI text-to-image workflows, not general LLM or agent-orchestration tasks.

Risk: The skill runs local commands and can write generated outputs to disk.

Mitigation: Keep output paths explicit and review proposed shell commands before execution.

Risk: Binding ComfyUI to a network interface can expose the local service beyond the machine.

Mitigation: Prefer binding ComfyUI to localhost unless intentional LAN access is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/comfyui-painter-tool-free)
- [Stable Diffusion v1.5 checkpoint](https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local ComfyUI execution and image file output; generated images are produced by the local ComfyUI environment.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
