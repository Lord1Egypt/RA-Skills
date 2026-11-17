## Description:

Plan complete Japan trips with flights, hotels, attractions, visa information, JR Pass context, and booking links powered by FlyAI and Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to plan Japan travel by collecting trip parameters, running FlyAI CLI searches, and formatting real-time flight, hotel, attraction, and visa results into itinerary guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global FlyAI CLI, including a sudo fallback.

Mitigation: Use only in an isolated, nonprivileged environment, do not allow automatic sudo installation, and prefer a pinned and verified FlyAI CLI.

Risk: The skill uses shell-style command templates with user-controlled values.

Mitigation: Review generated commands before execution and keep user-provided travel parameters quoted and constrained to the expected FlyAI CLI arguments.

Risk: Travel planning may prompt users for sensitive passport, payment, or personal identifiers.

Mitigation: Avoid entering sensitive identifiers unless FlyAI CLI logging and data handling are clear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/flyai-plan-japan-travel)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, tables, and inline shell command fallbacks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses FlyAI CLI results for prices, availability, and booking links; may include manual retry commands when data retrieval fails.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
