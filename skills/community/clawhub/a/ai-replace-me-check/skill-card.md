## Description:

通过苏格拉底追问方式提取用户隐性 SOP 知识，生成 AS-IS + TO-BE 可视化流程图和配置文件组。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwei03804-a11y](https://clawhub.ai/user/wwei03804-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations-focused users use this skill to map repeated work into an AS-IS process, design a TO-BE automation plan, and generate OpenClaw configuration drafts from their answers. It is aimed at SOP extraction, workflow bottleneck analysis, automation recommendations, and agent configuration planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends a curl-to-shell installer and unpinned npx installation commands.

Mitigation: Verify the source, version, and integrity of installation commands before running them, and prefer pinned versions where available.

Risk: Generated OpenClaw configuration may overwrite or persistently change project behavior.

Mitigation: Treat generated configuration as a draft, keep it project-scoped, review diffs, and back up existing configuration before applying changes.

Risk: Automation recommendations may enable scheduled tasks or external-data access before the user has reviewed the operational impact.

Mitigation: Require explicit approval before enabling scheduled automation, external-data access, or actions that affect live workflows.

## Reference(s):

- [Output Guide](references/output-guide.md)
- [Mermaid Diagram Template](references/mermaid-template.md)
- [Example Outputs](references/example-outputs.md)
- [ClawHub Skill Page](https://clawhub.ai/wwei03804-a11y/skills/ai-replace-me-check)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with ASCII diagrams, markdown files, HTML summary guidance, shell command snippets, and OpenClaw configuration drafts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from user answers and may include SOUL.md, USER.md, AGENTS.md, TOOLS.md, HEARTBEAT.md, IDENTITY.md, skills-recommendations.md, skill-creation-prompt.md, automation-suggestions.md, and summary.html.]

## Skill Version(s):

2.3.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
