## Description:

设计框架自动生成套件（框架生成器）：收到设计需求后自动生成完整设计框架并发送群预览

This skill is ready for commercial/non-commercial use.

## Publisher:

[807209066](https://clawhub.ai/user/807209066)

### License/Terms of Use:

MIT-0

## Use Case:

Design automation users can use this skill to turn Telegram design requests into a complete design framework, generated image prompt, and group preview for confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design requirements, reference images, generated prompts, and previews may be transmitted to Telegram and OpenRouter through the companion sender workflow.

Mitigation: Use only with information approved for those services, and avoid confidential client or product plans until data boundaries are explicit.

Risk: The skill depends on external sender scripts whose credentials handling, endpoints, attachment behavior, and lock cleanup are not proven by the artifact.

Mitigation: Review the exact design-framework-sender implementation and configuration before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/807209066/skills/design-framework-builder)
- [Publisher profile](https://clawhub.ai/user/807209066)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown-style design framework and prompt text delivered through shell-driven Telegram preview workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send design requirements, reference images, generated prompts, and previews through configured Telegram and OpenRouter services.]

## Skill Version(s):

2.0.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
