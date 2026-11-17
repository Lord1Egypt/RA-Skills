## Description:

A collection of skills for image and video generation and editing, covering model selection, prompt design, parameter tuning, batch processing, ComfyUI workflows, and cloud APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-repo](https://clawhub.ai/user/skills-repo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to plan and execute image and video generation or editing, then prepare media for delivery with reusable workflows and batch-processing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A locally hosted ComfyUI server may be reachable over the network if exposed without access controls.

Mitigation: Bind local use to localhost. For intentional remote access, configure authentication and network restrictions first.

Risk: Media sent to cloud generation services may be received by the selected provider.

Mitigation: Choose an approved provider and review its data terms before submitting media.

Risk: Batch processing can place generated or converted files alongside source media.

Mitigation: Use a separate batch-output directory to preserve originals.

Risk: Downloaded models, custom nodes, or dependencies may introduce unreviewed content; external dependencies were not tested.

Mitigation: Review downloaded dependencies before installing or running them.

## Reference(s):

- [ComfyUI workflow playbook](references/comfyui-workflow-playbook.md)
- [Image generation playbook](references/image-generation-playbook.md)
- [Video generation playbook](references/video-generation-playbook.md)
- [ClawHub release](https://clawhub.ai/skills-repo/skills/ai-media-generation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with prompts, workflow JSON, code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation and editing results depend on the selected models or providers; review visual quality and usage rights before delivery.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
