## Description:

Documentation reference for Bootstrap 5.3.8 that helps agents look up syntax, classes, usage, components, utilities, layout, forms, and Sass variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kens-agents](https://clawhub.ai/user/kens-agents)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill as a read-only Bootstrap 5.3.8 reference for checking component syntax, utility classes, layout behavior, form patterns, Sass variables, and migration details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation snippets and CDN or npm examples could be copied into a project without adequate review.

Mitigation: Treat examples as reference material and review them in the target project's security, dependency, and compatibility context before use.

Risk: Bootstrap guidance may be incorrect if applied to a project using a different Bootstrap version.

Mitigation: Confirm the project uses Bootstrap 5.3.8 before applying class, component, Sass variable, or migration guidance from this skill.

Risk: Answers about interactive Bootstrap components can omit runtime requirements such as JavaScript bundles or Popper.js.

Mitigation: Check the referenced Bootstrap category and slug for component-specific JavaScript and dependency requirements before implementation.

## Reference(s):

- [Bootstrap 5.3 Documentation](https://getbootstrap.com/docs/5.3/)
- [Bootstrap Documentation Index](scripts/bootstrap-reference.json)
- [Bootstrap Sass Variables](scripts/bootstrap-variables.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown answers with cited Bootstrap category and slug plus concise code examples when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only reference lookup; no commands, credentials, persistence, or privileged actions required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
