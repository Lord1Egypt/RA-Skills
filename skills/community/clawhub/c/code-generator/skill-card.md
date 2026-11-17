## Description:

Multi-language code generator for functions, classes, API endpoints, CRUD operations, tests, refactoring suggestions, and language conversion guides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold common code patterns, boilerplate, tests, REST endpoints, CRUD operations, and conversion or refactoring guidance from short descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated code or scaffolding may be incomplete, incorrect, or unsuitable for production use.

Mitigation: Review generated code before running, committing, or deploying it.

Risk: Prompt descriptions or project identifiers can be written to local command history by the secondary script.

Mitigation: Avoid passing secrets or confidential project names, and clear or redirect the local history location when needed.

Risk: Some generated web templates include development settings such as Flask debug mode.

Mitigation: Disable debug settings and harden generated services before deployment.

## Reference(s):

- [Code Generator on ClawHub](https://clawhub.ai/xueyetianya/skills/code-generator)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated snippets and templates should be reviewed before execution or deployment.]

## Skill Version(s):

2.3.4 (source: server release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
