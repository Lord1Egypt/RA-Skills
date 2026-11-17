## Description:

Create distinctive, production-grade static sites with React, Tailwind CSS, and shadcn/ui from plain text requirements, including Vite and Next.js workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiepco](https://clawhub.ai/user/aiepco)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agents use this skill to turn plain text website requirements into production-ready static web UI with React, Tailwind CSS, and shadcn/ui. It is intended for landing pages, marketing sites, portfolios, dashboards, and similar frontend builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initializer and bundling workflows may download and execute mutable npm or npx packages.

Mitigation: Run the workflow in a clean project or sandbox, review generated files before committing or deploying, and pin npm/npx versions when reproducible builds are required.

Risk: Generated frontend output may miss accessibility, responsive layout, or brand requirements without human review.

Mitigation: Use the included design and mobile checklists, then validate accessibility, responsiveness, and visual fit before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiepco/skills/frontend-design-ultimate)
- [Design Philosophy](references/design-philosophy.md)
- [Mobile Patterns](references/mobile-patterns.md)
- [shadcn Components](references/shadcn-components.md)
- [Site Config Template](templates/site-config.ts)
- [shadcn/ui](https://ui.shadcn.com)
- [Tailwind CSS](https://tailwindcss.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated React/TypeScript project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and npm; supports Vite or Next.js project generation and optional single-file HTML bundling.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata and VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
