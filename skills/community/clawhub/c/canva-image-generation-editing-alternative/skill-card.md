## Description:

使用 Nano Banana Pro 为 Canva、Canva Magic Media 或在线模板设计工作流生成可继续排版的商业图片资产，并明确不控制 Canva 或代表官方合作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and design-oriented agents use this skill to create editable bitmap layers for website hero images, social visuals, presentation covers, posters, and multi-size marketing assets before final layout in Canva or another design tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and any selected reference images are sent to AI Hive for generation.

Mitigation: Use only approved prompts and reference images, avoid sensitive or unlicensed inputs, and install the skill only when AI Hive processing is acceptable.

Risk: The skill requires an AI Hive API key, either from an environment variable, CLI flag, or local configuration file.

Mitigation: Prefer environment variables or restricted local config, keep the key out of shared files, and rotate it if it is exposed.

Risk: Generated commercial visuals can contain inaccurate brand, product, layout, or licensing details.

Mitigation: Review outputs before use, keep logos and exact text in the downstream design tool, and verify product accuracy, rights, and brand approvals.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/canva-image-generation-editing-alternative)
- [AI Hive API Endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API Key Setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, image files]

**Output Format:** [Markdown guidance with inline bash commands; generated tasks may return JSON status and downloaded PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed Nano Banana Pro image model through AI Hive and can accept optional reference images.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
