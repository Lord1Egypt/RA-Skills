## Description:

把当日盘面工作包、组合工作包和用户约束合成留减清加顺序、仓位框架和次日执行剧本。适用于用户明确要处理持仓、想要调仓路径、或要从市场主线映射到组合动作的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[minguncle](https://clawhub.ai/user/minguncle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to convert fresh A-share market context, portfolio details, and user constraints into prioritized hold, trim, exit, observe, add, or replacement actions with next-day scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce actionable A-share portfolio and stock-handling suggestions that could influence trading decisions.

Mitigation: Treat outputs as informational planning support, verify market freshness and personal constraints, and do not treat the output as professional financial advice.

Risk: Missing or stale market and portfolio inputs can make detailed action sequencing unreliable.

Mitigation: Require fresh market context and calibrated portfolio details before final conclusions; when inputs are incomplete, provide only a framework or request the missing information.

Risk: Overly aggressive position changes can increase concentration and timing risk.

Mitigation: Keep action plans conditional, include invalidation conditions and core risks, and avoid all-in or full-position switching recommendations.

## Reference(s):

- [Router Template](references/router-template.md)
- [A股动作路由 ClawHub skill page](https://clawhub.ai/minguncle/skills/a-share-action-router)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with scenario sections and action tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include a primary market scenario, hold/trim/exit/add table, handling order, target position structure, next-day playbook, and risk list.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
