## Description:

Run a WCAG 2.1 AA accessibility audit on a design or page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rolandpg](https://clawhub.ai/user/rolandpg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and product teams use this skill to review designs or pages against WCAG 2.1 AA criteria before handoff, including contrast, keyboard navigation, touch targets, form labels, alt text, and screen reader behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If connected design or project-tracker tools are enabled, the skill may use them while gathering accessibility details or preparing remediation tickets.

Mitigation: Confirm which tools are connected and require user confirmation before creating tickets or taking connector actions.

Risk: Agent-assisted accessibility review may miss issues that require real assistive-technology or keyboard testing.

Mitigation: Validate important findings with manual keyboard navigation, screen reader checks, contrast verification, and 200% zoom testing before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rolandpg/skills/accessibility-review)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown accessibility audit with findings tables and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WCAG criteria, severity labels, contrast checks, keyboard-navigation notes, screen-reader notes, and priority fixes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
