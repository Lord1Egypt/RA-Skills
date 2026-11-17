## Description:

Plans budget trips using flyai CLI data for low-cost flights, hotels, attractions, itinerary options, and travel-saving suggestions with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-focused agents use this skill to compare low-cost flights, budget lodging, points of interest, and itinerary options from flyai CLI results before choosing booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned global npm CLI dependency.

Mitigation: Review the flyai CLI source and package version first, pin the dependency, and avoid global installation where local or sandboxed execution is required.

Risk: The skill relies on externally supplied booking links.

Mitigation: Require explicit user confirmation before opening links, booking, purchasing, reserving, or submitting personal data, and validate destination URLs before use.

Risk: The skill can retain raw travel queries in a local execution log.

Mitigation: Avoid entering sensitive personal data, disclose local retention to users, and delete or disable local logs where policy requires.

Risk: Real-time travel data is unavailable when the flyai CLI or network access fails.

Mitigation: Report unavailable sections clearly, retry only through documented commands, and avoid filling gaps with unsourced travel data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/budget-trip-planner)
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif)
- [README](artifact/README.md)
- [Templates](artifact/references/templates.md)
- [Playbooks](artifact/references/playbooks.md)
- [Fallbacks](artifact/references/fallbacks.md)
- [Runbook](artifact/references/runbook.md)
- [Parent flyai skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, concise recommendations, and inline shell commands for setup or recovery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and should not include raw JSON.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
