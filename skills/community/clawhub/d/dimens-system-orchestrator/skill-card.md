## Description: <br>
用于维表智联系统级方案拆解与执行编排，适合“生成一个客户管理系统/平台”这类完整业务系统搭建需求。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyowl](https://clawhub.ai/user/flyowl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External builders and developers use this skill to plan complete Dimens business systems, including project structure, tables, documents, reports, permissions, workflows, and business scenario canvases before routing execution to the appropriate Dimens management skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real Dimens workspace changes that alter business data, permissions, workflows, reports, or public views. <br>
Mitigation: Use least-privilege Dimens credentials, require explicit confirmation before execution, and review the exact commands and affected resources before running them. <br>
Risk: Under-scoped defaults or public-view choices could expose business data. <br>
Mitigation: Design permissions before implementation, avoid public views unless explicitly required, and confirm visibility settings during post-action checks. <br>
Risk: Bulk updates, deletes, workflow publishing, and permission changes can have broad operational impact. <br>
Mitigation: Require separate confirmation for these actions and verify results with the relevant Dimens read-back commands after execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flyowl/dimens-system-orchestrator) <br>
- [Dimens official site](https://dimens.bintelai.com/) <br>
- [Authentication prerequisites](references/auth-prerequisite.md) <br>
- [Scenario taxonomy](references/scenario-taxonomy.md) <br>
- [System decomposition](references/system-decomposition.md) <br>
- [Business canvas flow](references/business-canvas-flow.md) <br>
- [Skill routing](references/skill-routing.md) <br>
- [Command mapping](references/command-mapping.md) <br>
- [Interface navigation](references/interface-navigation.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured plans, routing guidance, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Dimens CLI command sequences, resource IDs to verify, and canvas or system design outlines.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
