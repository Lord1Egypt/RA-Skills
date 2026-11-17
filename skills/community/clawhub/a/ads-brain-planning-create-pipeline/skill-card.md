## Description:

规划 Agent 新框架中的创编 Pipeline。面向新建投放方案生成，负责从经营诉求归一化出发，经过场景门禁、创建必要门禁、生成 launch_plan_draft，并委托 simple-create 生成 create_campaign。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizejia668-code](https://clawhub.ai/user/lizejia668-code)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and ad operations teams use this skill to structure Chinese-language new campaign planning flows. It guides an agent from request classification through eligibility checks, planning draft generation, campaign configuration handoff, warnings, and next-action selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign drafts may rely on assumptions for budget, audience, objective, eligibility, or missing business context.

Mitigation: Review the generated draft, warnings, and confirmation points before any downstream campaign creation action.

Risk: The workflow is intended for Chinese-language ad planning and may be unsuitable for other operating contexts.

Mitigation: Install and use it only where a Chinese-language campaign planning workflow matches the intended agent experience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizejia668-code/skills/ads-brain-planning-create-pipeline)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration, Guidance]

**Output Format:** [Chinese-language planning brief with JSON-compatible launch_plan_draft and create_campaign structures when eligible]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes warnings, assumptions, gate results, and next_action; does not directly execute campaign creation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
