## Description:

Plans backpacking trips with ultra-budget itineraries, hostel recommendations, multi-city routes, survival tips, and Fliggy-powered booking workflows for flights, hotels, trains, attractions, visas, insurance, and car rental.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to assemble backpacking routes, compare budget travel options, and produce booking-ready Markdown from flyai CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and run a global third-party flyai/Fliggy CLI before producing travel results.

Mitigation: Use a pinned, reviewed local installation and confirm the CLI package before enabling the skill in shared or production environments.

Risk: Trip requests may contain passport details, full names, credentials, or other sensitive travel information.

Mitigation: Avoid entering sensitive personal data unless logging and data handling are reviewed and controlled.

Risk: The artifact can persist raw trip queries locally in a flyai execution log when file writes are available.

Mitigation: Disable raw-query persistence or ensure generated logs are excluded from publication and handled under the user's data retention policy.

Risk: The skill forces commercial booking links and depends on live third-party travel data.

Mitigation: Review returned booking links and pricing before user action, and disclose failures or partial results instead of filling gaps from model knowledge.

## Reference(s):

- [Budget Backpacker Skill Page](https://clawhub.ai/xiejinsong/skills/budget-backpacker)
- [Publisher Profile: xiejinsong](https://clawhub.ai/user/xiejinsong)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output as the source for travel prices, availability, and booking links.]

## Skill Version(s):

3.2.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
