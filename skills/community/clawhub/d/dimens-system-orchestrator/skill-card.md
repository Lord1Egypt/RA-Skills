## Description:

用于维表智联系统级方案拆解与执行编排，适合完整业务系统、平台或管理应用的规划与落地路由。

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyowl](https://clawhub.ai/user/flyowl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, builders, and operations teams use this skill to turn broad Dimens business-system requests into project structure, tables, documents, reports, business-process canvases, permissions, workflows, and routed CLI execution steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to change business data, permissions, workflows, reports, and public views through Dimens CLI operations.

Mitigation: Use least-privilege API credentials and review each create, update, delete, permission, and public-view action before execution.

Risk: Secrets or API credentials could be exposed if pasted into chat or shell history.

Mitigation: Provide credentials through approved secret-handling paths and avoid placing real API keys or secrets in prompts, logs, generated files, or command history.

Risk: Generated public views or permissions may expose more project data than intended.

Mitigation: Default views and resources to private or role-restricted access unless broader sharing is explicitly required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flyowl/skills/dimens-system-orchestrator)
- [Dimens Official Website](https://dimens.bintelai.com/)
- [Scenario Taxonomy](artifact/references/scenario-taxonomy.md)
- [System Decomposition](artifact/references/system-decomposition.md)
- [Business Canvas Flow](artifact/references/business-canvas-flow.md)
- [Authentication Prerequisite](artifact/references/auth-prerequisite.md)
- [Skill Routing](artifact/references/skill-routing.md)
- [Command Mapping](artifact/references/command-mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI command examples, routing steps, and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project plans, resource IDs, post-execution verification steps, and risk notes when execution is requested.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
