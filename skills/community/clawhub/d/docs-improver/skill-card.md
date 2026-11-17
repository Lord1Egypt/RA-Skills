## Description:

Docs Improver helps agents assess technical documentation quality, generate missing project documents, check documentation-code consistency, and propose prioritized improvements across programming languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerry-guo-mys](https://clawhub.ai/user/jerry-guo-mys)

### License/Terms of Use:


## Use Case:

Developers and documentation maintainers use this skill to audit project documentation, generate standard docs such as README and API references, check consistency with code, and plan documentation improvements before releases or onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generation modes can overwrite existing README.md and docs files.

Mitigation: Review before installation on important repositories; run from a clean git worktree or separate output directory, and avoid combined or generation modes unless replacements are expected.

## Reference(s):

- [Documentation Best Practices](references/best-practices.md)
- [Documentation Style Guides](references/style-guides.md)
- [Mermaid Diagram Templates](assets/diagrams/mermaid-templates.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, generated documentation files, command-line summaries, and prioritized guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or replace README.md and files under docs/ when generation modes are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
