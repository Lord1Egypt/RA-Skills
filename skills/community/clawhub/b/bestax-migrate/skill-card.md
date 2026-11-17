## Description:

Guides developers migrating React apps from Bulma classes or older React Bulma libraries to @allxsmith/bestax-bulma using a codemod and source-specific mapping references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allxsmith](https://clawhub.ai/user/allxsmith)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to migrate React apps using Bulma classes, react-bulma-components, rbx, or bloomer to bestax-bulma, then review and resolve migration TODOs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated changes to dependencies and stylesheets may break builds or alter the interface.

Mitigation: Review the dry-run report and final diff, especially package.json and stylesheet imports; typecheck, build, and compare the rendered app.

Risk: Unresolved migration TODOs or retained imports can leave behavior incomplete or dependencies missing.

Mitigation: Resolve each TODO(bestax-migrate) using the source-specific references and verify remaining imports before installation.

## Reference(s):

- [Bestax: Migrate release](https://clawhub.ai/allxsmith/skills/bestax-migrate)
- [React Bulma Components migration maps](references/react-bulma-components/component-map.md)
- [rbx migration maps](references/rbx/component-map.md)
- [bloomer migration maps](references/bloomer/component-map.md)
- [Bulma classes migration maps](references/bulma-classes/component-map.md)
- [Stylesheet migration guidance](references/css-migration.md)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration guidance, Text]

**Output Format:** [Markdown with migration commands, review notes, and code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Codemod report and unresolved TODO(bestax-migrate) items require developer review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
