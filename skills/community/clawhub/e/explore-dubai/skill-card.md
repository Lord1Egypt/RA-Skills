## Description:

Plan Dubai trips using flyai CLI results for flights, hotels, attractions, itinerary planning, visa information, travel insurance, car rental, and related booking workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to find Dubai flights, lodging, attractions, and itinerary options from flyai CLI output with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned global npm CLI.

Mitigation: Review and install the flyai CLI manually from a trusted source, preferably pinned or isolated, before using the skill.

Risk: The workflow may retain raw prompts and travel details in a local execution log.

Mitigation: Treat execution logs as sensitive, avoid sharing them, and remove retained travel details when they are no longer needed.

Risk: The skill depends on a provider-specific booking workflow and live CLI results.

Mitigation: Use it only when that provider workflow is acceptable and verify current prices, policies, and booking details before purchase.

## Reference(s):

- [ClawHub Explore Dubai skill page](https://clawhub.ai/dingtom336-gif/skills/explore-dubai)
- [Parent flyai skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown travel results with booking links and inline shell commands when setup or retry steps are needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel data; results without detailUrl booking links are excluded.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
