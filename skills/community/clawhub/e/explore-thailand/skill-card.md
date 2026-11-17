## Description:

Plans Thailand travel using the FlyAI/Fliggy CLI for flights, hotels, attractions, itinerary planning, visa information, insurance, car rental, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to retrieve current Thailand travel options, compare flights, hotels, and attractions, and return Markdown summaries with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags forced vendor CLI use, global package installation, commercial booking links, and hidden local logging.

Mitigation: Install only when FlyAI/Fliggy-backed travel search is intended; prefer pinned, isolated CLI installation and review logging behavior before real booking workflows.

Risk: Travel planning can involve sensitive personal, payment, passport, or credential data.

Mitigation: Avoid entering sensitive details unless logging is removed or controlled and the booking workflow is trusted.

Risk: The skill depends on live flyai CLI output, so failures or unavailable coverage can lead to incomplete travel results.

Mitigation: Verify CLI installation before use, retry or simplify failed commands, and clearly mark partial results or limited coverage.

## Reference(s):

- [Explore Thailand ClawHub listing](https://clawhub.ai/dingtom336-gif/skills/explore-thailand)
- [README](README.md)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI results for travel data and should not output raw JSON.]

## Skill Version(s):

3.2.1 (source: server release evidence; artifact frontmatter states 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
