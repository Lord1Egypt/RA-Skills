## Description:

企业级 AI 图片生成指南，帮助代理配置和 run Doubao-based batch image generation workflows with multi-ratio output, style presets, prompt enhancement, quality checks, and automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, design operations teams, and automation teams use this skill to plan and configure batch image-generation workflows for ecommerce assets, marketing material, education content, game assets, and content review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad file, API, and command authority for image-generation automation.

Mitigation: Install and run it only in a dedicated image-generation workspace, and review requested actions before execution.

Risk: API credentials are needed for prompt enhancement or image-generation service access.

Mitigation: Provide scoped API keys through environment variables and avoid hardcoding secrets in scripts or configuration files.

Risk: Generated scripts or commands may write files to user-specified output paths.

Mitigation: Review Python commands, configuration paths, and archive destinations before allowing the agent to run them.

## Reference(s):

- [Detailed Reference](artifact/references/detail.md)
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/doubao-image-gen-tool-pro)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with YAML and JSON configuration examples, bash commands, and expected output file structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create image files, JSON reports, archived outputs, and workflow configuration files.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
