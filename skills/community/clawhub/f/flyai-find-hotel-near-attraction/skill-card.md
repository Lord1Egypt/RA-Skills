## Description:

Find hotels closest to a specific attraction, landmark, or scenic spot by verifying the POI, searching hotels through FlyAI/Fliggy, sorting by distance, and presenting booking links with POI context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to find hotels near a named attraction or landmark, with results grounded in FlyAI/Fliggy CLI output rather than model memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a commercial FlyAI/Fliggy CLI and may send destination, POI, date, and preference details to that service.

Mitigation: Tell users when an external CLI/service is used and avoid entering sensitive travel details unless they accept the service exposure.

Risk: The skill asks agents to install an unpinned global npm package and includes a sudo fallback.

Mitigation: Install the CLI manually from a trusted source, prefer a pinned version, and do not allow automatic sudo or global npm installation from the skill.

Risk: Hotel recommendations can be misleading if generated from model memory instead of live CLI results.

Mitigation: Require POI verification and hotel search command output before presenting hotel names, prices, ratings, distances, or booking links.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/flyai-find-hotel-near-attraction)
- [Fallbacks](references/fallbacks.md)
- [Playbooks](references/playbooks.md)
- [Runbook](references/runbook.md)
- [Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with CLI command execution and distance-sorted hotel tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hotel, POI, price, rating, distance, and booking-link details must come from FlyAI/Fliggy CLI output.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
