## Description:

Comprehensive guide for building enterprise-grade React and TypeScript component libraries and design systems from scratch, with Vue 3 patterns where applicable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldath](https://clawhub.ai/user/goldath)

### License/Terms of Use:

MIT-0

## Use Case:

Frontend developers and engineers use this skill to scaffold and govern component library work, including monorepo setup, design tokens, component standards, Storybook documentation, theming, testing, and publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples use mutable third-party package tooling such as latest package bootstraps.

Mitigation: Pin package versions, prefer locked devDependencies, and review generated changes before applying them to a production repository.

Risk: Release pipeline examples can expose publishing or project tokens to CI workflows.

Mitigation: Pass tokens only through scoped secrets or supported environment variables, restrict CI permissions, and pin GitHub Actions to reviewed versions or commit SHAs.

Risk: Automatic acceptance of visual-regression changes can approve unintended UI differences.

Mitigation: Use automatic baseline acceptance only during controlled initial setup and require human review for later visual updates.

## Reference(s):

- [Component Patterns Reference](references/component-patterns.md)
- [Release Pipeline Reference](references/release-pipeline.md)
- [Storybook Setup Reference](references/storybook-setup.md)
- [Testing Strategy Reference](references/testing-strategy.md)
- [Theming Reference](references/theming.md)
- [Design Tokens Reference](references/tokens.md)
- [Changesets](https://github.com/changesets/changesets)
- [Changesets GitHub Action](https://github.com/changesets/action)
- [Turborepo Schema](https://turbo.build/schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary stack is React and TypeScript; Vue 3 adaptations are included where applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
