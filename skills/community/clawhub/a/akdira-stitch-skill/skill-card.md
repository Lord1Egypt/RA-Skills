## Description:

Semantic Design System Skill for Google Stitch that generates agent-friendly DESIGN.md files enforcing strict typography, calibrated color, asymmetric layouts, motion intent, and anti-generic UI standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akdira](https://clawhub.ai/user/akdira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product designers use this skill to generate agent-friendly DESIGN.md guidance for Google Stitch screens, encoding a curated visual system with color, typography, layout, motion intent, and explicit UI anti-patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill applies strong opinionated design rules that may conflict with an existing brand, accessibility standard, localization requirement, or design system.

Mitigation: Review and edit the included font, color, layout, and anti-pattern rules before applying them to projects with established requirements.

Risk: Motion guidance is intended for downstream implementation even though Stitch generates static screens.

Mitigation: Treat motion specifications as handoff guidance and verify performance, accessibility, and reduced-motion behavior during implementation.

## Reference(s):

- [Stitch Skill on ClawHub](https://clawhub.ai/akdira/skills/akdira-stitch-skill)
- [Google Stitch](https://labs.google/stitch)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown file named DESIGN.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable design guidance covering visual atmosphere, color, typography, components, layout, responsive behavior, motion intent, and banned UI patterns.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and auto changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
