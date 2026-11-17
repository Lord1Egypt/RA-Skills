## Description:

Community Launch Runner helps agents prepare launch submission packages for Product Hunt, Show HN, Reddit, directories, and regional channels, with platform-rule checks and red-line guidance against vote solicitation or coordinated engagement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Launch teams, founders, and marketing operators use this skill to draft platform-specific community and directory launch materials, select channels by audience and region, and check submission plans against current community rules before launch day.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Platform rules and submission field requirements can change before launch day.

Mitigation: Require current checks against each platform's official rules or docs before finalizing submission materials.

Risk: Launch plans could cross community-policy lines by soliciting votes, coordinating engagement, or offering prohibited incentives.

Mitigation: Run the red-line check and remove any vote solicitation, engagement-ring language, delete-and-retry tactics, or incentives not explicitly allowed by the platform.

Risk: The skill can propose memory saves or launch-registry status events that should not be persisted without review.

Mitigation: Require explicit user approval before saving summaries or submitting registry proposal events.

## Reference(s):

- [Community Launch Runner on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/community-launch-runner)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Channel Matrix](artifact/references/channel-matrix.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown plans, tables, platform-specific submission drafts, red-line checks, and handoff summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current platform-rule verification; memory saves and launch-registry proposal events require explicit user approval.]

## Skill Version(s):

19.0.0 (source: evidence.release.version, SKILL.md frontmatter, metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
