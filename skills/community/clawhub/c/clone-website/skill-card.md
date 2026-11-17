## Description:

Clone, copy, rebuild, or reverse engineer any website for permitted website recreation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and web teams use this skill to document and rebuild websites they own or have explicit permission to reproduce. It guides browser-based reconnaissance, asset extraction, component specification, implementation, and responsive QA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support exact website copying, which may enable unauthorized reproduction, misleading lookalike sites, or misuse of third-party branding and media.

Mitigation: Use only for sites the operator owns or has explicit permission to reproduce, and avoid copying third-party branding, text, logos, media, or layouts in a way that could mislead users.

Risk: The setup workflow includes unpinned npm commands and project dependencies.

Mitigation: Run setup and build commands in an isolated project, review generated dependency changes, and pin dependency versions before deployment.

Risk: Generated rebuilds may introduce inaccurate UI behavior, accessibility regressions, or security issues if accepted without review.

Mitigation: Review specifications and generated code, scan outputs, and complete build, type-check, and responsive QA before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/clone-website)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project files, research notes, component specifications, and build or QA commands during agent execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
