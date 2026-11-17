## Description:

Accessibility Tester specializes in WCAG 2.1 and 2.2 accessibility checks, including screen reader compatibility, keyboard navigation, color contrast, and ARIA validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alshowse-tech](https://clawhub.ai/user/alshowse-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to generate accessibility testing guidance and structured WCAG-oriented reports for web application validation. It is best treated as a supporting accessibility review aid rather than a standalone compliance gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can report successful WCAG compliance without actually inspecting the supplied target.

Mitigation: Treat results as advisory until the implementation uses real browser and DOM inspection against the target under test.

Risk: Accessibility criteria may be marked as passed when they were not tested.

Mitigation: Require output to clearly distinguish tested, untested, failed, and simulated results before using it for release decisions.

Risk: Using the skill as a compliance gate could create misleading audit evidence.

Mitigation: Use fail-closed behavior for untested criteria and require human accessibility review or a trusted audit tool for compliance signoff.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alshowse-tech/skills/accessibility-tester)
- [Publisher profile](https://clawhub.ai/user/alshowse-tech)
- [WCAG 2.1: Non-text Content](https://www.w3.org/WAI/WCAG21/Understanding/non-text-content.html)
- [WCAG 2.1: Contrast Minimum](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown and JSON-style accessibility report content with code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WCAG status, issue severity, element details, scores, remediation guidance, and CI threshold examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
