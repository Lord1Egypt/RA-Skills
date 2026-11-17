## Description:

Design Taste Frontend guides agents through brief-driven frontend design for landing pages, portfolios, and redesigns, including appropriate design-system choices, audit-first redesigns, and pre-flight quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akdira](https://clawhub.ai/user/akdira)

### License/Terms of Use:

MIT-0

## Use Case:

Frontend developers and agents use this skill to create landing pages, portfolios, and redesigns with brief-driven visual direction, appropriate design-system choices, accessibility checks, and pre-flight quality review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide agents to add frontend dependencies or run design-system scaffolding commands.

Mitigation: Approve dependency installs explicitly, pin package versions where practical, and review generated project changes before committing or deploying.

Risk: The skill may direct agents to use external image, logo, or placeholder asset sources.

Mitigation: Confirm asset licenses, availability, and suitability before using generated or external assets in production.

Risk: Frontend design guidance can produce misleading or inappropriate implementation changes if applied without review.

Mitigation: Review and scan generated code, commands, and configuration before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/akdira/skills/design-taste-frontend-condensed)
- [Material Web](https://m3.material.io/develop/web)
- [Fluent UI Web Components](https://learn.microsoft.com/en-us/fluent-ui/web-components/)
- [Carbon Design System](https://carbondesignsystem.com/)
- [GOV.UK Frontend](https://github.com/alphagov/govuk-frontend)
- [U.S. Web Design System](https://github.com/uswds/uswds)
- [Tailwind CSS v4](https://tailwindcss.com/blog/tailwindcss-v4)
- [MDN CSS Grid Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend frontend dependencies, design-system packages, asset sources, accessibility checks, and project-specific implementation changes.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
