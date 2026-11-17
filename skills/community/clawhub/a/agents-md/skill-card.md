## Description:

帮助开发者依据项目目标、工程约束和真实失败，创建、审查或更新 AGENTS.md、CLAUDE.md 等仓库指令，并核实规则的作用域和验证依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mc0571](https://clawhub.ai/user/mc0571)

### License/Terms of Use:

MIT-0

## Use Case:

开发者在创建、审查、重构或更新仓库 Agent 指令时，用它从已核实的项目事实和工程经验中提炼可执行规则，并检查适用范围与验证方式。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changes to repository instruction files can affect future agent behavior.

Mitigation: Invoke deliberately for instruction-maintenance work and review diffs before keeping changes.

Risk: Inventorying an unauthorized repository could expose its file structure.

Mitigation: Run the optional read-only inventory script only against repositories you are authorized to inspect.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mc0571/skills/agents-md)
- [工程知识发现](artifact/references/discovery.md)
- [规则设计](artifact/references/rule-design.md)
- [验证与加载](artifact/references/validation.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Markdown repository instructions or review guidance; optional JSON inventory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese by default; preserves commands, paths, and identifiers as written.]

## Skill Version(s):

0.1.1 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
