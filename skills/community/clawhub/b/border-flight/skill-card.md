## Description:

Searches cross-border and international flights through the flyai CLI and formats real-time travel results with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search international routes, compare fares, and present booking-ready flight options based on live flyai CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports an unpinned global CLI install requirement.

Mitigation: Review and approve dependency installation before use; prefer a pinned and verified flyai CLI package.

Risk: The security summary reports commercial booking-link output and branding.

Mitigation: Disclose provider relationships and verify that booking links are appropriate for the deployment context.

Risk: The security summary reports hidden local logging of raw travel queries.

Mitigation: Avoid entering sensitive travel details unless logging behavior is reviewed and acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/border-flight)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, visa reminders, and inline shell commands when troubleshooting is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for flight results; raw JSON should not be shown to users.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
