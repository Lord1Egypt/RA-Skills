## Description:

Reviews frontend interfaces for WCAG 2.2 AA accessibility issues across semantics, keyboard navigation, focus, screen readers, and touch interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Frontend developers and accessibility reviewers use this skill to inspect interfaces, identify barriers against WCAG 2.2 AA, and prepare prioritized findings with suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad accessibility-related triggers may activate a review when one was not intended.

Mitigation: Confirm audit scope before inspecting UI or code paths.

Risk: An automated review may overlook barriers in keyboard or assistive-technology use.

Mitigation: Verify critical paths with a keyboard and at least one assistive technology or equivalent check before treating findings as complete.

## Reference(s):

- [Accessibility inspection report template](references/report-template.md)
- [Screen reader testing guide](references/screen-reader-testing.md)
- [Project homepage (package metadata)](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Code]

**Output Format:** [Markdown accessibility review with file-and-line findings and suggested code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be saved to reports/accessibility-review-YYYY-MM-DD-HHmmss.md.]

## Skill Version(s):

2.9.0 (source: release metadata, README.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
