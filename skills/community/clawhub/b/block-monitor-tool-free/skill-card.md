## Description:

AI生成内容验证与策略检查工具,支持黑白名单管理、内容分类与基础策略执行,适合个人开发者内容审核。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual builders use this skill to check AI-generated content against basic blocklist and allowlist rules, classify sensitive content, and record validation results before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist previews of sensitive user content in local verification logs.

Mitigation: Disable logging, redact previews, or avoid processing secrets, regulated data, and confidential content unless logging behavior is changed.

Risk: The skill has broad activation language for a tool with read and command execution access.

Mitigation: Invoke it only for explicit content moderation, rule management, and validation tasks, and review proposed shell commands before execution.

Risk: Filtering examples can create local *_filtered.txt files.

Mitigation: Check target paths and existing filtered files before running filtering commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/block-monitor-tool-free)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline Python and bash code blocks, plus JSON-style validation result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local rule files, verification logs, and filtered text files when the agent executes the provided examples.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
