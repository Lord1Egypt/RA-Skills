## Description:

Discover preserved ancient towns, water villages, and traditional settlements with real-time travel results and booking links through the FlyAI CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travel-focused agent users use this skill to search for ancient towns, water villages, and traditional settlements, then present real-time FlyAI results with booking links. It also guides installation, parameter collection, fallback handling, and output validation for FlyAI CLI travel searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and using a third-party FlyAI CLI for travel searches.

Mitigation: Require explicit approval before npm or npx commands and prefer a pinned or isolated CLI install.

Risk: The skill can log raw user queries to a hidden local execution log.

Mitigation: Disable or delete the local log unless query logging is intentionally desired, and avoid entering sensitive personal or booking details.

Risk: The skill uses shell-style command templates with user-supplied city names and keywords.

Mitigation: Review generated commands before execution and keep user inputs quoted and limited to supported parameters.

## Reference(s):

- [Ancient Town Explorer ClawHub Page](https://clawhub.ai/xiejinsong/skills/ancient-town-explorer)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FlyAI CLI output as the data source; responses should include booking links when results are shown.]

## Skill Version(s):

1.0.0 (source: release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
