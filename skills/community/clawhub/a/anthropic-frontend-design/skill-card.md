## Description:

Creates distinctive, production-grade frontend interfaces using design intelligence, accessibility and UX guidance, and bold aesthetic direction to avoid generic AI-generated design patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qrucio](https://clawhub.ai/user/qrucio)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill when designing or implementing frontend components, pages, applications, and interface systems. It helps select visual direction, design-system guidance, and implementation checks for accessible, distinctive UI work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional persistence can write Markdown files outside the intended design-system folder when crafted project, page, or output path values are used.

Mitigation: Use search-only mode by default; when persisting, use simple names made of letters, numbers, hyphens, or underscores and review generated paths before relying on the files.

Risk: Command examples returned from bundled CSV guidance may include package-runner suggestions that should not be executed blindly.

Mitigation: Treat returned commands as suggestions for review, and inspect them before running them in a project.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qrucio/skills/anthropic-frontend-design)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text guidance with code snippets, shell command examples, and optional generated Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search commands read bundled design guidance; persistence mode can create design-system Markdown files.]

## Skill Version(s):

1.1.0 (source: evidence release and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
