## Description:

Book birthday trip flights, surprise travel and celebration flight deals with birthday getaway booking, with related travel support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-booking agents use this skill to search birthday-trip flight options, compare results, and present booking links with birthday-oriented travel tips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run a third-party flyai CLI globally.

Mitigation: Review the CLI package before installation, require explicit install consent, and prefer a release that pins the package version.

Risk: Travel searches and booking-link selection depend on a third-party provider.

Mitigation: Tell users that live travel data and booking links come from the provider, and avoid using the skill unless that data sharing is acceptable.

Risk: Raw travel query details may be written to a hidden local execution log.

Mitigation: Disable, redact, or periodically remove local logs that contain user travel details.

Risk: Under-scoped shell-command authority can increase execution risk.

Mitigation: Validate parameters before command execution and avoid shell interpolation when constructing CLI calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/birthday-trip)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, booking links, birthday tips, and inline shell commands when recovery guidance is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flight results to come from flyai CLI output and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
