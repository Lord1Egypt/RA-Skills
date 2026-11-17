## Description:

Form Builder Pro helps agents create and validate dynamic JSON Schema forms with YAML configuration, conditional logic, custom validation, and Jinja2 rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate, configure, render, and validate application forms backed by JSON Schema and YAML definitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom Jinja2 template rendering can be unsafe when templates or form definitions come from untrusted sources.

Mitigation: Use only trusted templates and form definitions unless the renderer is changed to use sandboxing, autoescaping, strict validation, and pinned dependencies.

Risk: The server security verdict is suspicious for use in web-facing or multi-user environments.

Mitigation: Review the skill before installation in those environments and apply the server security guidance before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/skills/form-builder-pro)
- [Project Homepage](https://github.com/kaiyuelv/form-builder-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown or text with Python code snippets, JSON Schema, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated form definitions, validation results, rendered HTML, and implementation guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
