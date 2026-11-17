## Description:

Activity Planner helps users generate Chinese-language event plans with strategy, timelines, budgets, promotional copy, scripts, monitoring, staffing, risk plans, and evaluation as a structured HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonomi2](https://clawhub.ai/user/simonomi2)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, event operators, and business users use this skill to turn event requirements into executable plans for launches, annual meetings, pop-up events, promotions, community activities, and trade shows. The skill collects required event details and produces a ready-to-review HTML plan covering execution, promotion, materials, risk response, and measurement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may contain user-provided business details or untrusted text.

Mitigation: Review where reports are saved, sanitize or escape user-provided values before opening or sharing HTML, and treat generated reports as documents that require human review.

## Reference(s):

- [Activity Framework](references/activity_framework.md)
- [Budget Guide](references/budget_guide.md)
- [Copywriting Templates](references/copywriting_templates.md)
- [Promotion Monitor](references/promotion_monitor.md)
- [Script Templates](references/script_templates.md)
- [HTML Plan Template](assets/plan_template.html)

## Skill Output:

**Output Type(s):** [Text, HTML, Guidance, Files]

**Output Format:** [Structured HTML report with tables, timelines, scripts, copy blocks, monitoring sections, and review sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is saved as a local HTML file in the user's current working directory.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
