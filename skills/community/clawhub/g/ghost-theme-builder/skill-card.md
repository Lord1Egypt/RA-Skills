## Description:

Build, customize, review, debug, migrate, and optimize Ghost CMS Handlebars themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frontendweb](https://clawhub.ai/user/frontendweb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, customize, review, debug, migrate, and optimize production Ghost CMS themes using Handlebars templates, Ghost helpers, routing, memberships, search, accessibility, SEO, and GScan validation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Starter-kit, npm, npx, and global install commands can fetch or run mutable third-party code.

Mitigation: Pin external repositories and packages, review package scripts, prefer the minimal bundled theme shape when possible, and run dependency installs in a constrained project environment.

Risk: Generated membership, newsletter, and analytics features can create consent or privacy gaps if site behavior is unclear.

Mitigation: Make consent and privacy behavior explicit in the generated theme and align those features with the site's Ghost settings before deployment.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/frontendweb/skills/ghost-theme-builder)
- [Ghost CMS](https://ghost.org)
- [TryGhost Theme Documentation](https://github.com/TryGhost/Docs/tree/main/themes)
- [Theme Structure](docs/structure.md)
- [GScan](docs/gscan.md)
- [Ghost Contexts](reference/contexts.md)
- [Ghost Helpers](reference/helpers.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, file paths, configuration snippets, review findings, and validation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Ghost theme templates, partials, package.json settings, routes.yaml guidance, accessibility and SEO recommendations, and GScan validation steps.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
