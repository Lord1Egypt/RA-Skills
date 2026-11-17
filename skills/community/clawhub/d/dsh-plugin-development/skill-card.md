## Description:

This skill guides developers and AI agents through building, debugging, packaging, and publishing DSH/Cordis plugins, with templates and a version gate for the pre-stable upstream.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liupengyang-1008](https://clawhub.ai/user/liupengyang-1008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this guide to choose a DSH/Cordis plugin form, implement or troubleshoot plugin features, and package a plugin for distribution. It is development guidance and tooling, not an installable DSH plugin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some troubleshooting guidance approves all dependency scripts and keeps notes outside the project.

Mitigation: Use a separate development profile, approve dependency build scripts individually, keep recovery notes in the project unless shared agent memory is intended, pin external packages, forward only necessary credentials, and redact configurations before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liupengyang-1008/skills/dsh-plugin-development)
- [Project homepage](https://github.com/liupengyang-1008/dsh-plugin-development)
- [Version gate and freshness guidance](references/00-version-gate.md)
- [Plugin templates](references/02-templates.md)
- [API cookbook](references/03-api-cookbook.md)
- [Development and packaging workflow](references/06-workflow.md)
- [Scope and maintenance guidance](references/15-skill-scope-and-maintenance.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code templates, configuration examples, shell commands, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Version-specific examples should be checked against the target DSH release.]

## Skill Version(s):

1.8.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
