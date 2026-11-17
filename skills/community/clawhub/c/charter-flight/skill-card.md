## Description:

Book charter flights, private jet bookings, group charter aircraft, and related travel services using live flyai CLI results powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search charter-compatible route options, private-jet-style premium routes, and fallback flight searches via the flyai CLI. It formats live travel results into bookable Markdown while reminding users that actual charter or private jet booking requires direct operator or airline confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install the flyai CLI globally and fallback material mentions sudo installation.

Mitigation: Install and review the CLI in a controlled environment; do not allow automatic sudo or global package installation without explicit operator approval.

Risk: The security evidence flags vendor-only booking links and misleading charter framing.

Mitigation: Treat results as scheduled-flight references and verify actual charter or private jet availability directly with operators or airlines before booking.

Risk: The runbook describes local execution logging that could capture sensitive travel details.

Mitigation: Disable or tightly control logging before use with sensitive itineraries, and define retention and access controls for any travel logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/charter-flight)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output and booking links for listed results; should not provide travel results from model memory.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
