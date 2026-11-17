## Description:

Validate, diff, and export DESIGN.md files to ensure consistent design tokens, WCAG compliance, and design system integrity across projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flexrox](https://clawhub.ai/user/flexrox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and UI engineers use this skill to validate DESIGN.md files, compare design token changes, export tokens, and align component work with design system requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm install or npx execution may run a newer @google/design.md package than the reviewed release expected.

Mitigation: Prefer a pinned @google/design.md dependency in a project-local package.json with a lockfile before running commands.

Risk: The DESIGN.md CLI may read design files and write generated token outputs in the current project.

Mitigation: Run commands only in projects where that package is allowed to access those files, and review generated token files before use.

## Reference(s):

- [DESIGN.md specification](https://github.com/google-labs-code/design.md)
- [Stitch Tool](https://stitch.withgoogle.com/)
- [Design Tokens Format](https://www.designtokens.org/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation of JSON token export files when command output is redirected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
