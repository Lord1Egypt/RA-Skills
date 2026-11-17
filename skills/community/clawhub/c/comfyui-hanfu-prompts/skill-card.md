## Description:

14套已验证的 ComfyUI Z-Image 汉服写真、王家卫风格和杂志封面提示词模板，搭配双采样工作流生成高质量图像。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lantianbaicai](https://clawhub.ai/user/lantianbaicai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, designers, and ComfyUI users use this skill to select and run Hanfu portrait, Wong Kar-wai-inspired, and magazine-cover prompt templates for local Z-Image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented workflow depends on the external comfy-batch package.

Mitigation: Install in an isolated virtual environment or container, and pin or verify the package version before running commands.

Risk: The skill is a Chinese-language ComfyUI prompt pack, which may be harder for some operators to review accurately.

Mitigation: Translate and review prompts, workflow assumptions, and generated outputs before production or public use.

Risk: Artifact documentation references local NSFW templates and public sharing restrictions.

Mitigation: Keep sensitive outputs local unless they have been reviewed against applicable platform, workplace, and legal policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lantianbaicai/skills/comfyui-hanfu-prompts)
- [Skill instructions](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python import snippets, shell commands, and prompt-template names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local ComfyUI setup with Z-Image models and the external comfy-batch package.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
