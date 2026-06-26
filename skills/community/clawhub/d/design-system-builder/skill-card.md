## Description: <br>
Comprehensive guide for building enterprise-grade component libraries and design systems from scratch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goldath](https://clawhub.ai/user/goldath) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Frontend developers and design-system maintainers use this skill to plan, scaffold, and govern production component libraries. It covers design tokens, component API standards, Storybook documentation, theming, testing, and release workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CI and release snippets may publish to the wrong package, registry, or permissions scope if applied without review. <br>
Mitigation: Review package names, workflow permissions, registry targets, and token scopes before use; dry-run publishing before releasing packages. <br>
Risk: Credentialed workflows for npm, GitHub, and Chromatic can expose excessive access if broad tokens are used. <br>
Mitigation: Use least-privilege tokens and restrict release credentials to the intended repository, package scope, and workflow. <br>


## Reference(s): <br>
- [Component Patterns Reference](references/component-patterns.md) <br>
- [Design Tokens Reference](references/tokens.md) <br>
- [Storybook Setup Reference](references/storybook-setup.md) <br>
- [Theming Reference](references/theming.md) <br>
- [Testing Strategy Reference](references/testing-strategy.md) <br>
- [Release Pipeline Reference](references/release-pipeline.md) <br>
- [Changesets](https://github.com/changesets/changesets) <br>
- [Changesets GitHub Action](https://github.com/changesets/action) <br>
- [ClawHub Skill Page](https://clawhub.ai/goldath/design-system-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only design-system guidance for React and TypeScript, with Vue 3 notes where applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
