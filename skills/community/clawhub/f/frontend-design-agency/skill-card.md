## Description:

Use when building, redesigning, or extending web-app frontends that must look production-ready, visually distinctive, and systemically designed instead of like generic AI-generated UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arn0ld87](https://clawhub.ai/user/arn0ld87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design-minded agents use this skill to plan and implement production-ready web-app frontends, including design direction, tokens, component code, responsive behavior, accessibility checks, and quality gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is opinionated and may steer frontend work toward React, TypeScript, Tailwind, and shadcn-style implementations even when another stack is a better project fit.

Mitigation: Confirm the target stack and existing design system before applying generated code or configuration.

Risk: Design guidance and generated UI proposals can still be visually, accessibility, or product-fit incorrect for a specific application.

Mitigation: Review outputs against the bundled quality gate, accessibility checklist, and project requirements before deployment.

Risk: Bundled evaluator files are QA artifacts rather than required runtime behavior.

Mitigation: Keep evaluator artifacts out of production paths unless they are intentionally used for review.

## Reference(s):

- [Research Workflow](references/research-workflow.md)
- [Visual Direction Canvas](references/visual-direction-canvas.md)
- [Design System Rules](references/design-system-rules.md)
- [Quality Gate](references/quality-gate.md)
- [Product Requirements Checklist](references/product-requirements-checklist.md)
- [Accessibility Checklist](references/accessibility-checklist.md)
- [Generic vs Distinctive Examples](references/generic-vs-distinctive-examples.md)
- [Motion System Guide](references/motion-system-guide.md)
- [Color Palette Decision Framework](references/color-palette-examples.md)
- [Typography Scale Template](references/typography-scale-template.md)
- [Grid System Template](references/grid-system-template.md)
- [Layout Patterns Library](references/layout-patterns-library.md)
- [Breakpoint Definition](references/breakpoint-definition.md)
- [Focus States Template](references/focus-states-template.md)
- [User Persona Template](references/user-persona-template.md)
- [Component Template](references/component-template.tsx)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include visual direction notes, design tokens, React or TypeScript component code, implementation assumptions, responsive notes, and quality checks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
