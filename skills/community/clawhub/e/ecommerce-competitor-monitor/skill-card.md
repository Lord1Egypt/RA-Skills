## Description:

电商竞品价格监控系统 monitors competitor product pages across ecommerce platforms, tracks price, inventory, and promotion changes, and alerts users when configured thresholds are met.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhao123-dot](https://clawhub.ai/user/lijinhao123-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, operations agencies, and brand teams use this skill to configure recurring competitor price monitoring, compare results against saved baselines, and receive alerts or summary reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring monitoring jobs may continue after setup without clear lifecycle controls.

Mitigation: Confirm the check interval and alert channel before enabling monitoring, and document how to list, stop, and delete any scheduled jobs.

Risk: Saved baselines, screenshots, and history can retain product-page data longer than the user expects.

Mitigation: Confirm storage locations up front and provide a deletion path for saved history and page captures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijinhao123-dot/skills/ecommerce-competitor-monitor)
- [ClawHub publisher profile](https://clawhub.ai/user/lijinhao123-dot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, monitoring alerts, and tabular reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create scheduled checks, saved baselines, screenshots, and historical monitoring records when the host agent provides those tools.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
