## Description:

Front End Dev helps agents create distinctive, production-grade static web interfaces with React, Tailwind CSS, shadcn/ui, and Vite or Next.js workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tysnyder](https://clawhub.ai/user/tysnyder)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agents use this skill to turn plain-language site requirements into production-oriented React, Tailwind CSS, and shadcn/ui implementations, including landing pages, marketing sites, portfolios, dashboards, and static web UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: npm-based scaffolding scripts and npx commands can execute package code during setup.

Mitigation: Run initialization and bundling in a clean project directory or sandbox, pin package and CLI versions where stricter control is required, and review generated lockfiles before use.

Risk: Generated frontend projects may modify or add many local files as part of scaffolding and bundling.

Mitigation: Use a fresh workspace without unrelated secrets or source files, then review generated code and configuration before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tysnyder/skills/front-end-design)
- [Design Philosophy](references/design-philosophy.md)
- [Mobile Patterns](references/mobile-patterns.md)
- [shadcn Components](references/shadcn-components.md)
- [Site Config Template](templates/site-config.ts)
- [shadcn/ui documentation](https://ui.shadcn.com)
- [Tailwind CSS documentation](https://tailwindcss.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated React, TypeScript, Tailwind CSS, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May scaffold Vite or Next.js projects and optionally bundle static output into a single HTML file.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
