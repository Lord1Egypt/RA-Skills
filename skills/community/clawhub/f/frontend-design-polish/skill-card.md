## Description:

Helps agents design, review, polish, and iterate production-grade frontend interfaces across websites, dashboards, app shells, components, onboarding, accessibility, responsiveness, typography, motion, and visual systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyafeichina](https://clawhub.ai/user/liyafeichina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design-focused agents use this skill to plan, critique, build, and refine frontend interfaces with attention to visual hierarchy, UX copy, accessibility, responsive behavior, theming, motion, performance, and production polish.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that live-mode helpers may expose project files.

Mitigation: Review before installing and avoid live mode on untrusted repositories, sensitive local projects, or authenticated production pages.

Risk: The security summary reports that a crafted project may be able to run commands through live-mode behavior.

Mitigation: Prefer a patched release that removes shell interpolation, pins npx usage, and enforces project-root containment for reads and writes.

Risk: The security guidance calls out live token and local-server origin handling.

Mitigation: Use live mode only in trusted local sessions and prefer a patched version that validates local-server origins and protects the live token.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liyafeichina/skills/frontend-design-polish)
- [Skill Definition](artifact/SKILL.md)
- [Craft Workflow](artifact/reference/craft.md)
- [Shape Workflow](artifact/reference/shape.md)
- [Critique Workflow](artifact/reference/critique.md)
- [Audit Workflow](artifact/reference/audit.md)
- [Live Mode Workflow](artifact/reference/live.md)
- [Brand Register Guidance](artifact/reference/brand.md)
- [Product Register Guidance](artifact/reference/product.md)
- [Color and Contrast Guidance](artifact/reference/color-and-contrast.md)
- [Responsive Design Guidance](artifact/reference/responsive-design.md)
- [Command Metadata](artifact/scripts/command-metadata.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command snippets, reports, design briefs, and configuration or source-file changes when applied by an agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to read or write project design context files and, in live mode, use a local browser helper for visual iteration.]

## Skill Version(s):

3.0.6 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
