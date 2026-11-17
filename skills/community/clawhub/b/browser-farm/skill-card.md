## Description:

Provides agents with a multi-account Chrome browser fleet for persistent login sessions, page automation, snapshots and rollback, monitoring scripts, structured extraction, and authenticated request replay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yysws5566](https://clawhub.ai/user/yysws5566)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to automate authorized web accounts across persistent Chrome profiles, including dashboard checks, repetitive page actions, table monitoring, structured extraction, and testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with high confidence and reports cookie disclosure, browser-process termination, and account-binding risks.

Mitigation: Follow the supplied security guidance: avoid installation until cookie replay, browser-process cleanup, and account binding are addressed or independently reviewed.

Risk: The scan is partial: only half of the listed components were scanned, some static analyzers were degraded, and referenced paths were missing.

Mitigation: Treat the scan as incomplete and obtain a complete independent review before relying on the skill.

## Reference(s):

- [Browser Farm on ClawHub](https://clawhub.ai/yysws5566/skills/browser-farm)
- [Agent integration guide](artifact/references/AGENTS.md)
- [Project overview](artifact/references/README.md)
- [Version history](artifact/references/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, JSON, Screenshots]

**Output Format:** [Text and JSON results, JPEG screenshots, and executable shell or HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser results vary with the requested operation and the target page.]

## Skill Version(s):

0.1.23 (source: frontmatter, CHANGELOG, ClawHub release evidence; released 2026-11-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
